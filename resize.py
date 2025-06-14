import os
import shutil
from PIL import Image

widths = [512, 768]
heights = [512, 768]
path = "./data./Original_size"

for width in widths:
    for height in heights:
        output_path = f"./data./{width}_{height}"
        os.makedirs(output_path, exist_ok=True)

        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if not os.path.isdir(folder_path):
                continue

            output_folder_path = os.path.join(output_path, folder)
            os.makedirs(output_folder_path, exist_ok=True)

            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                output_file_path = os.path.join(output_folder_path, file)

                if file.lower().endswith(".jpg"):
                    try:
                        with Image.open(file_path) as img:
                            resized = img.resize((width, height), Image.LANCZOS)
                            resized.save(output_file_path)
                            print(f"Resized: {file}")
                    except Exception as e:
                        print(f"Failed to process {file}: {e}")

                elif file.lower().endswith(".txt"):
                    try:
                        shutil.copyfile(file_path, output_file_path)
                        print(f"Copied txt: {file}")
                    except Exception as e:
                        print(f"Failed to copy {file}: {e}")