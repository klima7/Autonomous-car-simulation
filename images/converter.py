import os
import cv2


SOURCE_DIR = 'original'
TARGET_DIR = 'gray16'


def img_conversion(source_path, target_path):
    original = cv2.imread(source_path)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (16, 16), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(target_path, resized)


def get_images_count(directory):
    count = 0
    for dirpath, dnames, fnames in os.walk(directory):
        for f in fnames:
            if f.endswith(".png"):
                count += 1
    return count


def start():
    total_count = get_images_count(SOURCE_DIR)
    done_count = 0

    for dirpath, dnames, fnames in os.walk(SOURCE_DIR):
        for f in fnames:
            if f.endswith(".png"):
                source_path = os.path.join(dirpath, f)
                rel_source_path = os.path.relpath(source_path, SOURCE_DIR)
                target_path = os.path.join(TARGET_DIR, rel_source_path)

                target_dir = os.path.dirname(target_path)
                os.makedirs(target_dir, exist_ok=True)

                img_conversion(source_path, target_path)
                done_count += 1

                percent = done_count / total_count * 100
                print(f'{percent:.2f}')


start()
