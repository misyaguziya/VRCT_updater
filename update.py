
import os
import sys
import shutil
import tempfile
import webbrowser
from zipfile import ZipFile
import subprocess
from typing import Callable
import requests
import psutil

# fille name
DOWNLOAD_FILENAME = 'VRCT.zip'
DOWNLOAD_CUDA_FILENAME = 'VRCT_cuda.zip'
START_EXE_NAME = 'VRCT.exe'

# ファイルのダウンロード
GITHUB_API_URL = "https://api.github.com/repos/misyaguziya/VRCT/releases/latest"
GITHUB_URL = "https://github.com/misyaguziya/VRCT/releases/latest"

# 削除するファイル
DELETION_FILES = ["VRCT.exe", "backend.exe", "_internal"]

def taskKill():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == START_EXE_NAME:
                proc.terminate()
                proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def updateProcess(url, root_dir, cuda=False, callback_download=None, callback_extract=None):
    res = requests.get(url)
    assets = res.json()['assets']

    if cuda is True:
        filename = DOWNLOAD_CUDA_FILENAME
    else:
        filename = DOWNLOAD_FILENAME

    url = [i["browser_download_url"] for i in assets if i["name"] == filename][0]
    with tempfile.TemporaryDirectory() as tmp_path:
        # ファイルのダウンロード
        res = requests.get(url, stream=True)
        file_size = int(res.headers.get('content-length', 0))
        total_chunk = 0
        with open(os.path.join(tmp_path, filename), 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024*1000):
                file.write(chunk)
                total_chunk += len(chunk)
                if isinstance(callback_download, Callable):
                    callback_download([total_chunk, file_size])
                # print(f"downloaded {total_chunk}/{file_size}")

        # 旧ファイルの削除
        for file in os.listdir(root_dir):
            if file in DELETION_FILES:
                path = os.path.join(root_dir, file)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        # ファイルの解凍
        with ZipFile(os.path.join(tmp_path, filename)) as zf:
            extracted_counter = 0
            extracted_files = len(zf.infolist())
            for file_info in zf.infolist():
                extracted_counter += 1
                zf.extract(file_info, root_dir)
                if isinstance(callback_extract, Callable):
                    callback_extract([extracted_counter, extracted_files])

def init(callback_init=None):
    if isinstance(callback_init, Callable):
        callback_init()

def error(callback_error=None):
    if isinstance(callback_error, Callable):
        callback_error()
    webbrowser.open(GITHUB_URL)

def restart(callback_restart=None):
    subprocess.Popen(os.path.join(os.path.dirname(sys.executable), START_EXE_NAME))
    if isinstance(callback_restart, Callable):
        callback_restart()

def quit(callback_quit=None):
    if isinstance(callback_quit, Callable):
        callback_quit()

def update(cuda=False, callback_init=None, callback_download=None, callback_extract=None, callback_error=None, callback_restart=None, callback_quit=None):
    # task kill update program
    taskKill()
    # try update VRCT at most 5 times
    for i in range(5):
        try:
            init(callback_init)
            root_dir = os.path.dirname(sys.executable)
            updateProcess(GITHUB_API_URL, root_dir, cuda, callback_download, callback_extract)
            restart(callback_restart)
            break
        except Exception:
            import traceback
            with open('error.log', 'a') as f:
                traceback.print_exc(file=f)
        if i == 4:
            error(callback_error)
    quit(callback_quit)
    return True

if __name__ == '__main__':
    root_dir = os.path.dirname(sys.executable)

    updateProcess(GITHUB_API_URL, root_dir, False, lambda x: print(f"downloaded {x[0]}/{x[1]}"), lambda x: print(f"extracted {x[0]}/{x[1]}%"))