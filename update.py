
import os
import sys
import shutil
import tempfile
import webbrowser
from zipfile import ZipFile
from subprocess import Popen
from typing import Callable
import requests

# fille name
DOWNLOAD_FILENAME = 'VRCT.zip'
START_EXE_NAME = 'VRCT.exe'
TMP_DIR_NAME = 'tmp_update'

# ファイルのダウンロード
GITHUB_URL = "https://api.github.com/repos/misyaguziya/VRCT/releases/latest"
BOOTH_URL = "https://misyaguziya.booth.pm/"

# 削除しないデータ
EXCLUDE_DATA = ["config.json", "update.exe", "logs", "weights", TMP_DIR_NAME]

def removeFiles(root_dir, callback=None):
    for file in os.listdir(root_dir):
        if file in EXCLUDE_DATA:
            continue

        if isinstance(callback, Callable):
            callback(file)
        print("removeFiles", file)

        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def copyFiles(root_dir, callback=None):
    tmp_path = os.path.join(root_dir, TMP_DIR_NAME)
    for root, dirs, files in os.walk(tmp_path):
        for dir in dirs:
            os.makedirs(os.path.join(root_dir, os.path.relpath(os.path.join(root, dir), tmp_path)), exist_ok=True)
            print("copytreeWithCallback", os.path.join(root_dir, os.path.relpath(os.path.join(root, dir), tmp_path)))
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(root_dir, os.path.relpath(src_file, tmp_path))
            shutil.copy2(src_file, dst_file)
            if callback:
                callback(file)
            print("copytreeWithCallback", dst_file)
    shutil.rmtree(os.path.join(root_dir, TMP_DIR_NAME))

def downloadFile(url, root_dir, callback_download=None, callback_extract=None):
    res = requests.get(url)
    assets = res.json()['assets']
    url = [i["browser_download_url"] for i in assets if i["name"] == DOWNLOAD_FILENAME][0]
    with tempfile.TemporaryDirectory() as tmp_path:
        res = requests.get(url, stream=True)
        file_size = int(res.headers.get('content-length', 0))
        total_chunk = 0
        with open(os.path.join(tmp_path, DOWNLOAD_FILENAME), 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024*1000):
                file.write(chunk)
                total_chunk += len(chunk)
                if isinstance(callback_download, Callable):
                    callback_download([total_chunk, file_size])
                print(f"downloaded {total_chunk}/{file_size}")

        with ZipFile(os.path.join(tmp_path, DOWNLOAD_FILENAME)) as zf:
            total_files = len(zf.infolist())
            extracted_files = 0
            for file_info in zf.infolist():
                extracted_files += 1
                zf.extract(file_info, os.path.join(root_dir, TMP_DIR_NAME))
                if isinstance(callback_extract, Callable):
                    callback_extract([extracted_files, total_files])
                print(f"extracted {extracted_files}/{total_files}")

def update(callback_download=None, callback_extract=None, callback_remove=None, callback_copy=None, callback_success=None, callback_quit=None):
    try:
        root_dir = os.path.dirname(sys.executable)
        downloadFile(GITHUB_URL, root_dir, callback_download, callback_extract)
        removeFiles(root_dir, callback_remove)
        copyFiles(root_dir, callback_copy)
        if isinstance(callback_success, Callable):
            callback_success()
        Popen(os.path.join(root_dir, START_EXE_NAME))
    except Exception as e:
        print(e)
        webbrowser.open(BOOTH_URL)
    finally:
        if isinstance(callback_quit, Callable):
            callback_quit()
    return True

if __name__ == '__main__':
    root_dir = os.path.dirname(sys.executable)
    downloadFile(GITHUB_URL, root_dir, lambda x: print(f"downloaded {x[0]}/{x[1]}"), lambda x: print(f"extracted {x[0]}/{x[1]}%"))
    removeFiles(root_dir, lambda x: print(f"removeFiles {x}"))
    copyFiles(root_dir, lambda x: print(f"copyFiles {x}"))
    Popen(os.path.join(root_dir, START_EXE_NAME))
    webbrowser.open(BOOTH_URL)