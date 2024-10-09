from threading import Thread
from update import update
from ui import UpdatingWindow

# ウィンドウの作成
app = UpdatingWindow()
app.showUpdatingWindow()

def downloadCallback(values):
    app.updateDownloadProgress(values, "downloading")

def extractCallback(values):
    app.updateDownloadProgress(values, "extracting")

def errorCallback():
    app.updateDownloadProgress([], "error")

def restartCallback():
    app.updateDownloadProgress([], "restarting")

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