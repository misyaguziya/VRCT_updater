from threading import Thread
import customtkinter
from update import update


# ウィンドウの作成
app = customtkinter.CTk()
app.geometry("350x100")
app.resizable(False, False)  # ウィンドウのサイズを固定
app.overrideredirect(True)  # タイトルバーを非表示にする

# ウィンドウを画面の中央に配置
window_width = 350
window_height = 100
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
app.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# タスクバーにアプリを最前面に設定
app.attributes("-topmost", True)
app.after(100, lambda: app.attributes("-topmost", False))  # 0.1秒後に最前面設定を解除

# グリッドの行と列の重みを設定
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# プログレスバーの作成
progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal", mode="determinate", corner_radius=0, height=10)
progressbar.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

# ラベルの作成
label = customtkinter.CTkLabel(app)
label.grid(row=1, column=0, padx=20, pady=0, sticky="ew")

# プログレスバーの値を設定
progressbar.set(0)  # 0%の位置に設定
label.configure(text="Downloading...")

def downloadCallback(values):
    label.configure(text=f"Downloading files... {values[0]/values[1]*100:.2f}%({values[0]//1000}/{values[1]//1000})")
    progressbar.set(values[0]/values[1])

def extractCallback(values):
    label.configure(text=f"Extracting files... {values[0]/values[1]*100:.2f}%({values[0]}/{values[1]})")
    progressbar.set(values[0]/values[1])

def removeCallback(value):
    progressbar.configure(mode="indeterminnate")
    progressbar.start()
    label.configure(text=f"Removing old files... {value}")

def copyCallback(value):
    progressbar.configure(mode="indeterminnate")
    progressbar.start()
    label.configure(text=f"Copying new files... {value}")

def successCallback():
    label.configure(text="Success!")

def quitCallback():
    app.quit()

th_update = Thread(target=update, args=(downloadCallback, extractCallback, removeCallback, copyCallback, successCallback, quitCallback))
th_update.daemon = True
th_update.start()

# メインループの開始
app.mainloop()