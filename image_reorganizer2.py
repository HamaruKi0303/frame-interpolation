from PIL import Image
import os
import shutil
from tqdm import tqdm

def resize_image(image_path, size):
    with Image.open(image_path) as img:
        img_resized = img.resize(size)
    return img_resized

def reorganize_images(src_folder, dest_folder, num_images_per_set, new_size):
    print("""
    ┏━━━━━━━━━━━━━━━━━━━┓
    ┃ (｡･ω･｡)つ━☆・*。 ┃
    ┃ ⊂　　 ノ 　　　・゜+.┃
    ┃ しーＪ　　　°。+ *´¨)┃
    ┃.· ´¸.·*´¨) ¸.·*¨)    ┃
    ┃(¸.·´ (¸.·'* ☆ Let's  ┃
    ┃        Reorganize!    ┃
    ┗━━━━━━━━━━━━━━━━━━━┛
    """)

    image_files = [f for f in os.listdir(src_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()
    
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    prev_last_img = None  
    counter = 1  

    for i in tqdm(range(0, len(image_files), num_images_per_set), desc="Reorganizing"):
        new_folder = os.path.join(dest_folder, f'set_{i // num_images_per_set + 1:04d}')
        if(os.path.exists(new_folder)):
            return True
        os.mkdir(new_folder)
        
        if prev_last_img:
            new_file_name = f"{counter:04d}_{prev_last_img}"
            resized_img = resize_image(os.path.join(src_folder, prev_last_img), new_size)
            resized_img.save(os.path.join(new_folder, new_file_name))
            counter += 1  

        for j in range(i, min(i + num_images_per_set, len(image_files))):
            new_file_name = f"{counter:04d}_{image_files[j]}"
            resized_img = resize_image(os.path.join(src_folder, image_files[j]), new_size)
            resized_img.save(os.path.join(new_folder, new_file_name))
            counter += 1  
        
        if i + num_images_per_set - 1 < len(image_files):
            prev_last_img = image_files[i + num_images_per_set - 1]
        else:
            prev_last_img = None

if __name__ == "__main__":
    src_folder = "/output/txt2img/2023-09-03/Mechanical-Owls-of-the-Chaotic-Fantasy-Realm_mov_up2"  # 例: "C:/path/to/images"
    dest_folder = "/output/txt2img/2023-09-03/Mechanical-Owls-of-the-Chaotic-Fantasy-Realm_mov_up2_reo"  # 例: "C:/path/to/destination"
    num_images_per_set = 2  
    new_size = (600, 900)  # 新しい画像のサイズ（この場合は800x600にリサイズ）

    reorganize_images(src_folder, dest_folder, num_images_per_set, new_size)
    
    print("☆*:.｡.o(≧▽≦)o.｡.:*☆ Done!")
