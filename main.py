from threading import Thread
import customtkinter
from update import update
from ui import UpdatingWindow
from PIL import Image

# ウィンドウの作成
app = customtkinter.CTk()
# app.resizable(False, False)  # ウィンドウのサイズを固定
# app.overrideredirect(True)  # タイトルバーを非表示にする
app.withdraw()  # ウィンドウを表示しない

# ウィンドウを画面の中央に配置
window_width = 0
window_height = 0
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
app.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

def quitCallback():
    app.quit()
    app.destroy()

updating_window = UpdatingWindow(vrct_gui=app)
updating_window.showUpdatingWindow()

def downloadCallback(values):
    updating_window.updateDownloadProgress(values[0]/values[1], "downloading")

def extractCallback(values):
    updating_window.updateDownloadProgress(values[0]/values[1], "extracting")

th_update = Thread(target=update, args=(downloadCallback, extractCallback, None, None, None, quitCallback))
th_update.daemon = True
th_update.start()

# メインループの開始
app.mainloop()