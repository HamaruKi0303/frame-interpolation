import os
import subprocess
import glob

import os
import sys

from tqdm import tqdm
import pprint

from image_reorganizer2 import reorganize_images

sys.path.append("/data/frame-interpolation")
from eval.interpolator_cli import main
import eval.interpolator_cli


animatoranon_film_folder = "/data/frame-interpolation/film.sh"
src_folder = "/output/txt2img/2023-09-07/Mechanical-Falcons_up"  # 例: "C:/path/to/images"
target_dit = f"{src_folder}_reo"

film_executable = os.path.basename(animatoranon_film_folder.strip())
film_folder = os.path.dirname(animatoranon_film_folder.strip())

num_images_per_set = 2
# new_size = (600, 900)  # 新しい画像のサイズ（この場合は800x600にリサイズ）
# new_size = (972, 1728)  # 新しい画像のサイズ（この場合は800x600にリサイズ）
# new_size = (756, 1344)  # 新しい画像のサイズ（この場合は800x600にリサイズ）
new_size = (540, 960)  # 新しい画像のサイズ（この場合は800x600にリサイズ）
reorganize_images(src_folder, target_dit, num_images_per_set, new_size)

print("☆*:.｡.o(≧▽≦)o.｡.:*☆ Done!")


l = glob.glob(f'{target_dit}/set*')
pprint.pprint(l)

for dir_path in tqdm(l):
        args = ["./" + film_executable,
                # "/output/img2img/MechanicalMirage",
                dir_path,
                "6",
                "30"
                ]

        print(f'film args       : {args}')
        print(f'dir_path        : {dir_path}')
        print(f'film_folder     : {film_folder}')

        # main()
        # pattern = '/output/img2img/20230724140133'
        # model_path = '/data/frame-interpolation/pretrained_models/film_net/Style/saved_model'
        # times_to_interpolate = 1
        # eval.interpolator_cli.run(pattern, model_path, times_to_interpolate)

        # # subprocess.call(args, cwd=film_folder, shell=True)
        subprocess.run(args, cwd=film_folder)
        # # # process.wait()
        # # # .stdoutに標準出力、.stderrに標準エラー出力が格納される
        # print(result.stdout)
        # print(result.stderr)


        # python /data/frame-interpolation/demo.py
        # python /data/frame-interpolation/demo.py 


import os
import subprocess

def concatenate_videos_in_directory(directory_path, fps=30):
    # 指定されたディレクトリ内のフォルダをソートして取得
    directories = sorted([os.path.join(directory_path, d) for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d)) and d.startswith("set_")])

    # interpolated.mp4 ファイルのパスを収集
    video_files = []
    for dir_name in directories:
        video_path = os.path.join(dir_name, "interpolated.mp4")
        if os.path.exists(video_path):
            video_files.append(video_path)

    # ffmpeg を使用して動画を結合
    if video_files:
        # 一時的にリストファイルを作成
        with open("temp_list.txt", "w") as f:
            for video in video_files:
                f.write(f"file '{video}'\n")
        
        # ffmpeg コマンドの実行
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "temp_list.txt", "-r", str(fps), "-c", "copy", "output.mp4"]
        subprocess.run(cmd)

        # 一時ファイルの削除
        os.remove("temp_list.txt")
    else:
        print("No interpolated.mp4 files found.")

# 例: '/path/to/your/folder' を実際のフォルダのパスに置き換え、desired_fps を希望のFPSに置き換えてください
desired_fps = 30
concatenate_videos_in_directory('/path/to/your/folder', fps=desired_fps)