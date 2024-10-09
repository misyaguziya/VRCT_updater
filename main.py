from threading import Thread
from customtkinter import CTk
from update import update
from ui import UpdatingWindow

# ウィンドウの作成
app = CTk()
app.resizable(False, False)  # ウィンドウのサイズを固定
app.overrideredirect(True)  # タイトルバーを非表示にする
app.withdraw()  # ウィンドウを表示しない

updating_window = UpdatingWindow(vrct_gui=app)
updating_window.showUpdatingWindow()

def downloadCallback(values):
    updating_window.updateDownloadProgress(values, "downloading")

def extractCallback(values):
    updating_window.updateDownloadProgress(values, "extracting")

def errorCallback():
    updating_window.updateDownloadProgress([], "error")

def restartCallback():
    updating_window.updateDownloadProgress([], "restarting")

def quitCallback():
    app.quit()
    app.destroy()

th_update = Thread(
    target=update,
    args=(
        downloadCallback,
        extractCallback,
        errorCallback,
        restartCallback,
        quitCallback)
    )
th_update.daemon = True
th_update.start()

# メインループの開始
app.mainloop()