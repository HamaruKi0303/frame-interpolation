import os
import subprocess
import glob
from tqdm import tqdm
import sys
from image_reorganizer2 import reorganize_images
from eval.interpolator_cli import main

# Constants
ANIMATOR_ANON_FILM_PATH = "/data/frame-interpolation/film.sh"
# SOURCE_FOLDER_PATH = "/output/txt2img/2023-09-12/MecaAN"
SOURCE_FOLDER_PATH = "/output/img2img/20230928032831"
TARGET_FOLDER_PATH = f"{SOURCE_FOLDER_PATH}_reo2"
IMG_SCALE = 0.7
IMAGE_SIZE = (int(1080*IMG_SCALE), int(1920*IMG_SCALE))
NUM_IMAGES_PER_SET = 2
DESIRED_FPS = 30
SYS_PATH_APPEND = "/data/frame-interpolation"

# Prepare environment
sys.path.append(SYS_PATH_APPEND)
film_executable_name = os.path.basename(ANIMATOR_ANON_FILM_PATH.strip())
film_folder_path = os.path.dirname(ANIMATOR_ANON_FILM_PATH.strip())

def organize_and_resize_images():
    """
    Organizes and resizes images.
    """
    reorganize_images(SOURCE_FOLDER_PATH, TARGET_FOLDER_PATH, NUM_IMAGES_PER_SET, IMAGE_SIZE)
    print("☆*:.｡.o(≧▽≦)o.｡.:*☆ Done!")

def generate_films_from_images():
    """
    Generates films from the organized and resized images.
    """
    image_sets = glob.glob(f'{TARGET_FOLDER_PATH}/set*')
    for image_set in tqdm(image_sets):
        is_file = os.path.isfile(f"{image_set}/interpolated.mp4")
        if is_file:
            print(f"interpolated.mp4 is a file.")
            continue

        args = [
            "./" + film_executable_name,
            image_set,
            "5",
            "30"
        ]
        subprocess.run(args, cwd=film_folder_path)

def concatenate_videos_in_directory(directory_path):
    """
    Concatenates videos present in the given directory.
    
    Args:
    - directory_path: Path to the directory containing video files to concatenate.
    """
    # Fetch sorted directories with set_ prefix
    directories = sorted([
        os.path.join(directory_path, d) for d in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, d)) and d.startswith("set_")
    ])

    video_files = [os.path.join(dir_name, "interpolated.mp4") for dir_name in directories if os.path.exists(os.path.join(dir_name, "interpolated.mp4"))]

    if not video_files:
        print("No interpolated.mp4 files found.")
        return

    with open("temp_list.txt", "w") as f:
        for video in video_files:
            f.write(f"file '{video}'\n")

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "temp_list.txt", "-r", str(DESIRED_FPS), "-c", "copy", "/output/output.mp4"]
    subprocess.run(cmd)

    os.remove("temp_list.txt")

if __name__ == "__main__":
    organize_and_resize_images()
    generate_films_from_images()
    concatenate_videos_in_directory(TARGET_FOLDER_PATH)
    # python /data/frame-interpolation/demo2.py 