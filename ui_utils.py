from os import path as os_path
from PIL import Image
from time import sleep

def getImagePath(file_name):
    # root\img\file_name
    return os_path.join(os_path.dirname(__file__), "img", file_name)

def getImageFileFromUiUtils(file_name):
    # root\img\file_name
    return Image.open(os_path.join(os_path.dirname(__file__), "img", file_name))

# This making gradient color process was made by ChatGPT.
def generateGradientColor(value, color_start, color_end):
    # 補完色を計算
    interpolated_color = [
        int(start + (end - start) * value) for start, end in zip(color_start, color_end)
    ]

    # RGB値を0から255の範囲にクリップ
    interpolated_color = [max(0, min(255, val)) for val in interpolated_color]

    # RGBを16進数に変換
    hex_color = "#{:02x}{:02x}{:02x}".format(*interpolated_color)

    return hex_color

def setGeometryToCenterOfScreen(root_widget):
    root_widget.update()
    sw=root_widget.winfo_screenwidth()
    sh=root_widget.winfo_screenheight()
    geometry_width = root_widget.winfo_width()
    geometry_height = root_widget.winfo_height()

    root_widget.geometry(str(geometry_width)+"x"+str(geometry_height)+"+"+str((sw-geometry_width)//2)+"+"+str((sh-geometry_height)//2))

def fadeInAnimation(root_widget, steps:int=10, interval:float=0.1, max_alpha:float=1):
    alpha_steps = 100
    alpha_steps*=max_alpha
    step_size = alpha_steps/steps
    root_widget.attributes("-alpha", 0)
    num = 0
    while num < alpha_steps:
        if not root_widget.winfo_exists():
            break
        root_widget.attributes("-alpha", num / 100)
        root_widget.update()
        sleep(interval)
        num += step_size
    root_widget.attributes("-alpha", max_alpha)