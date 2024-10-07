
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

# ファイルのダウンロード
GITHUB_URL = "https://api.github.com/repos/misyaguziya/VRCT_update_test/releases/latest"
BOOTH_URL = "https://misyaguziya.booth.pm/"

# 削除するファイル
DELETION_FILES = ["VRCT.exe", "backend.exe", "_internal"]

def updateProcess(url, root_dir, callback_download=None, callback_extract=None):
    res = requests.get(url)
    assets = res.json()['assets']
    url = [i["browser_download_url"] for i in assets if i["name"] == DOWNLOAD_FILENAME][0]
    with tempfile.TemporaryDirectory() as tmp_path:
        # ファイルのダウンロード
        res = requests.get(url, stream=True)
        file_size = int(res.headers.get('content-length', 0))
        total_chunk = 0
        with open(os.path.join(tmp_path, DOWNLOAD_FILENAME), 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024*1000):
                file.write(chunk)
                total_chunk += len(chunk)
                if isinstance(callback_download, Callable):
                    callback_download([total_chunk, file_size])
                # print(f"downloaded {total_chunk}/{file_size}")

        with ZipFile(os.path.join(tmp_path, DOWNLOAD_FILENAME)) as zf:
            extracted_files = len(zf.infolist())
            removed_files = len(DELETION_FILES)
            total_files = extracted_files + removed_files

        # 旧ファイルの削除
        removed_counter = 0
        for file in os.listdir(root_dir):
            if file in DELETION_FILES:
                if isinstance(callback_extract, Callable):
                    removed_counter += 1
                    callback_extract([removed_counter, total_files])
                # print(f"removeFiles {removed_counter}/{removed_files}")

                path = os.path.join(root_dir, file)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        # ファイルの解凍
        with ZipFile(os.path.join(tmp_path, DOWNLOAD_FILENAME)) as zf:
            extracted_counter = 0
            for file_info in zf.infolist():
                extracted_counter += 1
                zf.extract(file_info, root_dir)
                if isinstance(callback_extract, Callable):
                    callback_extract([extracted_counter, total_files])
                # print(f"extracted {extracted_counter}/{extracted_files}")

def restart(callback_restart=None):
    if isinstance(callback_restart, Callable):
        callback_restart()
    Popen(os.path.join(os.path.dirname(sys.executable), START_EXE_NAME))

def quit(callback_quit=None):
    if isinstance(callback_quit, Callable):
        callback_quit()

def update(callback_download=None, callback_extract=None, callback_restart=None, callback_quit=None):
    try:
        root_dir = os.path.dirname(sys.executable)
        updateProcess(GITHUB_URL, root_dir, callback_download, callback_extract)
        restart(callback_restart)
    except Exception as e:
        print(e)
        webbrowser.open(BOOTH_URL)
    finally:
        quit(callback_quit)
    return True

if __name__ == '__main__':
    root_dir = os.path.dirname(sys.executable)

    updateProcess(GITHUB_URL, root_dir, lambda x: print(f"downloaded {x[0]}/{x[1]}"), lambda x: print(f"extracted {x[0]}/{x[1]}%"))