
import os
import sys
import shutil
import tempfile
import webbrowser
from zipfile import ZipFile
from subprocess import Popen
from typing import Callable

# fille name
DOWNLOAD_FILENAME = 'VRCT.zip'
START_EXE_NAME = 'VRCT.exe'
TMP_DIR_NAME = 'tmp_update'

# ファイルのダウンロード
GITHUB_URL = "https://api.github.com/repos/misyaguziya/VRCT/releases/latest"
BOOTH_URL = "https://misyaguziya.booth.pm/"

# 削除しないファイル
EXCLUDE_FILES = ["logs", "config.json", "weights", "update.exe", TMP_DIR_NAME]

def removeFiles(root_dir):
    for file in os.listdir(root_dir):
        if file in EXCLUDE_FILES:
            continue
        path = os.path.join(root_dir, file)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def copyFiles(root_dir):
    shutil.copytree(os.path.join(root_dir, TMP_DIR_NAME), root_dir, dirs_exist_ok=True)
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
            for chunk in res.iter_content(chunk_size=1024*100):
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
        if isinstance(callback_remove, Callable):
            callback_remove()
        removeFiles(root_dir)
        if isinstance(callback_copy, Callable):
            callback_copy()
        copyFiles(root_dir)
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
    removeFiles(root_dir)
    copyFiles(root_dir)
    Popen(os.path.join(root_dir, START_EXE_NAME))
    webbrowser.open(BOOTH_URL)