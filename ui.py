import time
from customtkinter import CTkImage, CTkLabel, CTkToplevel, CTkProgressBar, CTkFrame
from ui_utils import getImageFileFromUiUtils, setGeometryToCenterOfScreen, fadeInAnimation, generateGradientColor, getImagePath, getFontPath
from PIL import ImageFont, ImageDraw, Image, ImageTk

class UpdatingWindow(CTkToplevel):
    def __init__(self, vrct_gui):
        super().__init__()
        self.withdraw()
        self.overrideredirect(True)
        self.configure(fg_color="#292a2d")
        self.title("Updating...")
        self.after(200, lambda: self.iconbitmap(getImagePath("vrct_logo_mark_black.ico")))
        self.is_showed_downloading_process = False
        self.is_showed_unpackaging_process = False
        BG_WIDTH= 300
        BG_HEIGHT= 350
        self.BG_HEX_COLOR = "#292a2d"
        self.TEXT_HEX_COLOR = "#f2f2f2"
        self.font = ImageFont.truetype(getFontPath('myFont.ttf'), 12)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.updating_background = CTkFrame(self, corner_radius=0, fg_color=self.BG_HEX_COLOR, width=BG_WIDTH, height=BG_HEIGHT)
        self.updating_background.grid()


        self.PROGRESSBAR_HEIGHT = 2
        self.PROGRESSBAR_WIDTH = 240
        self.PROGRESSBAR_Y = 240
        self.PROGRESSBAR_X = 30


        self.downloading_unpackaging_d = getImageFileFromUiUtils("downloading_unpackaging_d.png")
        self.downloading_unpackaging_d_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.downloading_unpackaging_d, size=(self.downloading_unpackaging_d.width, self.downloading_unpackaging_d.height))
        )


        self.downloading_unpackaging_u = getImageFileFromUiUtils("downloading_unpackaging_u.png")
        self.downloading_unpackaging_u_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.downloading_unpackaging_u, size=(self.downloading_unpackaging_u.width, self.downloading_unpackaging_u.height))
        )


        self.unpackage_img = getImageFileFromUiUtils("unpackage_icon.png")

        self.unpackage_img_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.unpackage_img, size=(self.unpackage_img.width, self.unpackage_img.height))
        )


        self.progressbar = CTkProgressBar(
            self.updating_background,
            height=self.PROGRESSBAR_HEIGHT,
            width=self.PROGRESSBAR_WIDTH,
            corner_radius=0,
            fg_color=self.BG_HEX_COLOR,
            progress_color=self.BG_HEX_COLOR,
        )
        self.progressbar.set(0)
        self.progressbar.place(x=self.PROGRESSBAR_X, y=self.PROGRESSBAR_Y, anchor="nw")


        self.chato_delivering_img = getImageFileFromUiUtils("chato_delivering.png")

        self.chato_delivering_img_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.chato_delivering_img, size=(self.chato_delivering_img.width, self.chato_delivering_img.height))
        )
        self.chato_delivering_img_label.place(x=-30, y=self.PROGRESSBAR_Y - 1, anchor="s")


        self.chato_unpackaging_img = getImageFileFromUiUtils("chato_unpackaging.png")

        self.chato_unpackaging_img_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.chato_unpackaging_img, size=(self.chato_unpackaging_img.width, self.chato_unpackaging_img.height))
        )
        self.chato_unpackaging_img_label.place(x=-30, y=self.PROGRESSBAR_Y + self.PROGRESSBAR_HEIGHT + 1, anchor="n")


        self.vrct_update_process_img = getImageFileFromUiUtils("vrct_update_process.png")

        self.vrct_update_process_img_label = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
            image=CTkImage(self.vrct_update_process_img, size=(self.vrct_update_process_img.width, self.vrct_update_process_img.height))
        )
        self.vrct_update_process_img_label.place(x=150, y=300, anchor="center")

        self.vrct_update_process_text = CTkLabel(
            self.updating_background,
            text=None,
            height=0,
            fg_color=self.BG_HEX_COLOR,
        )
        self.vrct_update_process_text.place(x=150, y=280, anchor="center")

    def updateDownloadProgress(self, values:list, progress_type:str):
        if progress_type == "downloading":
            progress = values[0] / values[1]
            if self.is_showed_downloading_process is False:
                self.downloading_unpackaging_d_label.place(x=50, y=56, anchor="nw")
                self.is_showed_downloading_process = True

            fg_color = generateGradientColor(
                value=progress,
                color_start=[242, 242, 242], # RGB values for #f2f2f2
                color_end=[72, 164, 149], # RGB values for #48a495
            )
            self.progressbar.configure(fg_color=fg_color)

            chato_x = self.PROGRESSBAR_X + (progress * self.PROGRESSBAR_WIDTH)
            self.chato_delivering_img_label.place(x=chato_x)
            self.progressbar.set(progress)

            text = f"{int(progress * 100)}% ({values[0]//1000//1000}MB/{values[1]//1000//1000}MB)"
            image_width, image_height = 300, 12
            image = Image.new("RGBA", (image_width, image_height))
            draw = ImageDraw.Draw(image)
            bbox  = draw.textbbox((0, 0), text=text, font=self.font)
            x = (image_width - bbox[2]) // 2
            y = (image_height - bbox[3]) // 2
            draw.text((x, y), text, font=self.font, fill=(242, 242, 242))
            tk_image = ImageTk.PhotoImage(image)
            self.vrct_update_process_text.configure(
                image=tk_image,
            )
            self.update_idletasks()

        elif progress_type == "extracting":
            progress = values[0] / values[1]
            if self.is_showed_unpackaging_process is False:
                self.chato_delivering_img_label.place_forget()
                self.downloading_unpackaging_u_label.place(x=50, y=56, anchor="nw")
                self.unpackage_img_label.place(x=130, y=174, anchor="nw")
                self.progressbar.configure(fg_color=self.BG_HEX_COLOR, progress_color="#4B4C4F")
                self.is_showed_unpackaging_process = True

            chato_x = (self.PROGRESSBAR_X - 3) + (self.PROGRESSBAR_WIDTH - (progress * self.PROGRESSBAR_WIDTH))
            self.chato_unpackaging_img_label.place(x=chato_x)
            self.progressbar.set(1 - progress)

            text = f"{int(progress * 100)}% ({values[0]}/{values[1]})"
            image_width, image_height = 300, 12
            image = Image.new("RGBA", (image_width, image_height))
            draw = ImageDraw.Draw(image)
            bbox  = draw.textbbox((0, 0), text=text, font=self.font)
            x = (image_width - bbox[2]) // 2
            y = (image_height - bbox[3]) // 2
            draw.text((x, y), text, font=self.font, fill=(242, 242, 242))
            tk_image = ImageTk.PhotoImage(image)
            self.vrct_update_process_text.configure(
                image=tk_image,
            )
            self.update_idletasks()

        elif progress_type == "restarting":
            text = "Restarting"
            for _ in range(5):
                self.chato_unpackaging_img_label.place_forget()
                image_width, image_height = 300, 12
                image = Image.new("RGBA", (image_width, image_height))
                draw = ImageDraw.Draw(image)
                bbox  = draw.textbbox((0, 0), text=text, font=self.font)
                x = (image_width - bbox[2]) // 2
                y = (image_height - bbox[3]) // 2
                draw.text((x, y), text, font=self.font, fill=(242, 242, 242))
                tk_image = ImageTk.PhotoImage(image)
                self.vrct_update_process_text.configure(
                    image=tk_image,
                )
                self.update_idletasks()
                text = text + "."
                time.sleep(1)

        elif progress_type == "error":
            text="Error! Can't Update software."
            self.chato_unpackaging_img_label.place_forget()
            image_width, image_height = 300, 12
            image = Image.new("RGBA", (image_width, image_height))
            draw = ImageDraw.Draw(image)
            bbox  = draw.textbbox((0, 0), text=text, font=self.font)
            x = (image_width - bbox[2]) // 2
            y = (image_height - bbox[3]) // 2
            draw.text((x, y), text, font=self.font, fill=(242, 242, 242))
            tk_image = ImageTk.PhotoImage(image)
            self.vrct_update_process_text.configure(
                image=tk_image,
            )
            self.update_idletasks()
            time.sleep(5)
            text="Please download the latest version from the website."
            self.chato_unpackaging_img_label.place_forget()
            image_width, image_height = 300, 12
            image = Image.new("RGBA", (image_width, image_height))
            draw = ImageDraw.Draw(image)
            bbox  = draw.textbbox((0, 0), text=text, font=self.font)
            x = (image_width - bbox[2]) // 2
            y = (image_height - bbox[3]) // 2
            draw.text((x, y), text, font=self.font, fill=(242, 242, 242))
            tk_image = ImageTk.PhotoImage(image)
            self.vrct_update_process_text.configure(
                image=tk_image,
            )
            self.update_idletasks()
            time.sleep(5)

    def showUpdatingWindow(self):
        self.attributes("-alpha", 0)
        self.deiconify()
        setGeometryToCenterOfScreen(root_widget=self)
        fadeInAnimation(self, steps=5, interval=0.02)


    def destroyUpdatingWindow(self):
        self.destroy()