import os
import shutil

def copystatic(from_path, to_path):
    if os.path.exists(from_path):
        if os.path.exists(to_path):
            shutil.rmtree(to_path)
    os.mkdir(to_path)
    for item in os.listdir(from_path):
        src = os.path.join(from_path, item)
        dst = os.path.join(to_path, item)
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            copystatic(src, dst)