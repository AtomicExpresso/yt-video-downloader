import customtkinter as ctk
from utils.utils import Utils
from utils.config import Config
from io import BytesIO
from requests import get
from tkinter.font import BOLD
from PIL import Image


# Handles video info frame
class VidInfo:
    def __init__(self, parent):
        self.parent = parent
        self.info: dict = None  # For handeling info state, its a dict of video info
        self.error: bool = False  # For handeling error state

    # Configure the grid
    def config_vid_grid(self) -> None:
        # Cols
        self.vid_frame.grid_columnconfigure(0, weight=0)
        self.vid_frame.grid_columnconfigure(1, weight=0)
        self.vid_frame.grid_columnconfigure(2, weight=1)
        # Rows
        self.vid_ct_frame.grid_rowconfigure(0, weight=0)
        self.vid_ct_frame.grid_rowconfigure(1, weight=0)
        self.vid_ct_frame.grid_rowconfigure(2, weight=0)

    def append_vid_widget(self) -> None:
        # Append widgets to grid
        self.vid_tn_frame.grid(column=0, row=0, padx=10, pady=10, sticky="n")
        self.vid_ct_frame.grid(column=1, row=0, padx=10, pady=10, sticky="n")
        self.vid_ct_opt_frame.grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.vid_info_frame.grid(column=2, row=0, padx=10, pady=10, sticky="e")
        self.vid_frame.grid(
            row=[self.parent.frames.main_frame.grid_size()[1]],
            column=0,
            columnspan=3,
            padx=20,
            pady=5,
            sticky="nsew",
        )

        # TN frame
        self.vid_thumbnail_lbl.grid(column=0, row=1, pady=0, padx=(20, 10), sticky="w")

        # CT frame
        self.vid_title_lbl.grid(
            column=0, row=0, columnspan=2, pady=(10, 10), padx=(20, 10), sticky="w"
        )

        self.vid_dl_option.grid(column=0, row=1, padx=(10, 0), sticky="w")
        self.vid_res_option.grid(column=1, row=1, padx=(10, 10), sticky="w")

        self.vid_duriation_lbl.grid(
            column=0, row=3, pady=(10, 10), padx=(10, 0), sticky="w"
        )
        self.vid_size_lbl.grid(
            column=1, row=3, pady=(10, 10), padx=(10, 10), sticky="w"
        )

        # info frame
        self.vid_info_btn.grid(column=0, row=0, pady=(10, 0), padx=(10, 10), sticky="w")
        self.vid_copyurl_btn.grid(
            column=0, row=1, pady=(10, 0), padx=(10, 10), sticky="w"
        )
        self.vid_delete_btn.grid(
            column=0, row=2, pady=(10, 10), padx=(10, 10), sticky="w"
        )

    def create_vid_frames(self) -> None:
        # --main vid frame
        self.vid_frame = ctk.CTkFrame(
            self.parent.frames.main_frame,
            fg_color=f"{Config.theme["colors"]["primary"]}",
        )
        # --thumbnail frame
        self.vid_tn_frame = ctk.CTkFrame(
            self.vid_frame, fg_color=f"{Config.theme["colors"]["primary"]}"
        )
        # --content frame
        self.vid_ct_frame = ctk.CTkFrame(
            self.vid_frame, fg_color=f"{Config.theme["colors"]["primary"]}"
        )
        # --option-ct-frame (goes in ct frame)
        self.vid_ct_opt_frame = ctk.CTkFrame(
            self.vid_ct_frame, fg_color=f"{Config.theme["colors"]["primary"]}"
        )
        # --info frame
        self.vid_info_frame = ctk.CTkFrame(
            self.vid_frame, fg_color=f"{Config.theme["colors"]["primary"]}"
        )

    def create_vid_labels(self) -> None:
        # top row of CT frame
        self.vid_thumbnail_lbl = ctk.CTkLabel(
            self.vid_tn_frame, text="", image=self.vid_thumbnail
        )
        # bottom row of CT frame
        self.vid_duriation_lbl = ctk.CTkLabel(
            self.vid_ct_opt_frame,
            text_color=Config.theme["text_colors"]["primary"],
            text=f"Duriation: {self.info["duriation"]}",
        )
        self.vid_size_lbl = ctk.CTkLabel(
            self.vid_ct_opt_frame,
            text_color=Config.theme["text_colors"]["primary"],
            text=f"Size: {self.info["size"]}",
        )

    def create_vid_images(self) -> None:
        infoImgPath = Utils.get_resource_path("images/info.png")
        linkImgPath = Utils.get_resource_path("images/link.png")
        trashImgPath = Utils.get_resource_path("images/trash.png")
        
        # info frame
        infoImgSrc = Image.open(infoImgPath)
        self.infoImg = ctk.CTkImage(light_image=infoImgSrc, size=(20, 20))
        linkImgSrc = Image.open(linkImgPath)
        self.linkImg = ctk.CTkImage(light_image=linkImgSrc, size=(20, 20))
        trashImgSrc = Image.open(trashImgPath)
        self.trashImg = ctk.CTkImage(light_image=trashImgSrc, size=(20, 20))

    def create_vid_btn(self) -> None:
        # first row of info frame
        self.vid_info_btn = ctk.CTkButton(
            self.vid_info_frame,
            image=self.infoImg,
            fg_color=f"{Config.theme["colors"]["secondary"]}",
            hover_color=f"{Config.theme["colors"]["button"]["default"]}",
            text="",
            bg_color="transparent",
            width=45,
            command=lambda: self.parent.info_clbck(self.index),
        )
        # second row of info frame
        self.vid_copyurl_btn = ctk.CTkButton(
            self.vid_info_frame,
            image=self.linkImg,
            fg_color=f"{Config.theme["colors"]["secondary"]}",
            hover_color=f"{Config.theme["colors"]["button"]["default"]}",
            text="",
            bg_color="transparent",
            width=45,
            command=lambda: self.parent.copy_video_url_clbck(self.index),
        )
        # last row of info frame
        self.vid_delete_btn = ctk.CTkButton(
            self.vid_info_frame,
            image=self.trashImg,
            fg_color=f"{Config.theme["colors"]["secondary"]}",
            hover_color=f"{Config.theme["colors"]["button"]["default"]}",
            text="",
            bg_color="transparent",
            width=45,
            command=lambda: self.delete_video(),
        )

    def create_vid_options(self) -> None:
        self.vid_dl_option = ctk.CTkOptionMenu(
            self.vid_ct_opt_frame,
            fg_color=f"{Config.theme["colors"]["secondary"]}",
            bg_color=f"{Config.theme["colors"]["secondary"]}",
            dropdown_fg_color=f"{Config.theme["colors"]["button"]["default"]}",
            dropdown_text_color=f"{Config.theme["text_colors"]["primary"]}",
            dropdown_hover_color=f"{Config.theme["colors"]["primary"]}",
            button_color=f"{Config.theme["colors"]["button"]["hover"]}",
            button_hover_color=f"{Config.theme["colors"]["button"]["hover"]}",
            values=[*Config.dl_options],
            command=lambda cur_val: self.parent.set_dl_single_clbck(
                txt=cur_val, i=self.index
            ),
        )
        self.vid_res_option = ctk.CTkOptionMenu(
            self.vid_ct_opt_frame,
            fg_color=f"{Config.theme["colors"]["secondary"]}",
            bg_color=f"{Config.theme["colors"]["secondary"]}",
            dropdown_fg_color=f"{Config.theme["colors"]["button"]["default"]}",
            dropdown_text_color=f"{Config.theme["text_colors"]["primary"]}",
            dropdown_hover_color=f"{Config.theme["colors"]["primary"]}",
            button_color=f"{Config.theme["colors"]["button"]["hover"]}",
            button_hover_color=f"{Config.theme["colors"]["button"]["hover"]}",
            values=[*Config.res_options],
            command=lambda cur_val: self.parent.set_dl_single_clbck(
                txt=cur_val, i=self.index
            ),
        )
        # Set vid option values to the ones selected
        self.vid_dl_option.set(Config.dl_cur_option)
        self.vid_res_option.set(Config.res_cur_option)

    def create_special_case(self) -> None:
        # --Index, used for changeing a single video res and dl type
        self.vid_index = ctk.CTkLabel(self.vid_ct_frame, text=f"{self.info["index"]}")
        # gets the text from vid_index
        self.index = int(self.vid_index.cget("text"))

    # Create video widgets
    def create_vid_widgets(self) -> None:
        # create frames
        self.create_vid_frames()
        # create special case
        self.create_special_case()
        # create labels
        self.shorten_txt_length()
        self.create_vid_labels()
        # Create options
        self.create_vid_options()
        # Create buttons
        self.create_vid_btn()

    # fetch video image
    def fetch_vid_thumbnail(self) -> None:
        # Download the image using requests
        image_url = self.info["thumbnail"]
        response = get(image_url)
        img_data = response.content

        vid_thumbnail_img = Image.open(BytesIO(img_data))
        self.vid_thumbnail = ctk.CTkImage(
            light_image=vid_thumbnail_img, size=(150, 120)
        )

    # Shortens text length
    def shorten_txt_length(self) -> None:
        # shorten video title if it suppasses 55 chars
        if len(self.info["title"]) < 55:
            self.vid_title_lbl = ctk.CTkLabel(
                self.vid_ct_frame,
                text=f"{self.info["title"]}",
                text_color=Config.theme["text_colors"]["primary"],
                font=("ariel", 13, BOLD),
            )
        else:
            self.vid_title_lbl = ctk.CTkLabel(
                self.vid_ct_frame,
                text=f"{self.info["title"][:55]}...",
                text_color=Config.theme["text_colors"]["primary"],
                font=("ariel", 13, BOLD),
            )

    def update_vid_info(self, new_info: dict) -> None:
        # change specified fields
        for key, value in new_info.items():
            if key in self.info:
                self.info[key] = value

        # Update the widgets
        if self.vid_title_lbl:
            self.shorten_txt_length()

        if self.vid_size_lbl:
            self.vid_size_lbl.configure(text=f"Size: {self.info['size']}")

    # Handles download in progress state
    def dl_in_progress(self) -> None:
        # destroy options to make room for progress bar
        self.vid_res_option.destroy()
        self.vid_dl_option.destroy()

        # create progress bar
        self.vid_dl_progress = ctk.CTkProgressBar(
            self.vid_ct_opt_frame,
            progress_color=f"{Config.theme["colors"]["progress"]}",
            orientation="horizontal",
            width=250,
        )
        self.vid_dl_progress_txt = ctk.CTkLabel(
            self.vid_ct_opt_frame,
            text="0%",
            text_color=Config.theme["text_colors"]["primary"],
            fg_color="transparent",
            font=("ariel", 15),
        )
        self.vid_dl_progress_txt.grid(column=0, row=1, padx=(10, 10), sticky="w")
        self.vid_dl_progress.grid(
            column=0, row=2, padx=(10, 0), columnspan=3, sticky="w"
        )

        self.vid_dl_progress.set(0)
        self.vid_dl_progress.update()

    # Set progress bar progress
    def set_progress(self, stream, chunk, bytes_remaining) -> None:
        total_size: str | int = stream.filesize
        bytes_downloaded: str | int = total_size - bytes_remaining
        percentage_left: str | int = bytes_downloaded / total_size * 100
        progess_per: int = int(percentage_left)
        # update progress text
        self.vid_dl_progress_txt.configure(text=f"{progess_per}%")
        self.vid_dl_progress_txt.update()
        # update progress bar
        self.vid_dl_progress.set(float(percentage_left) / 100)
        self.vid_dl_progress.update()

    # Runs after video download has been completed
    def set_complete(self, stream, chunk) -> None:
        # update progress text
        self.vid_dl_progress_txt.configure(
            text=f"Complete!", text_color=f"{Config.theme["colors"]["progress"]}"
        )
        self.vid_dl_progress.set(100)
        self.vid_dl_progress.update()
        self.parent.vid_dl_count += 1  # update videos downloaded counter

    # Handles errors for video
    def handle_error(self) -> None:
        self.error = True
        self.vid_frame.configure(
            border_color=f"{Config.theme["colors"]["error"]}", border_width=2
        )
        self.vid_dl_progress_txt.configure(
            text=f"Error", text_color=f"{Config.theme["colors"]["error"]}"
        )
        self.vid_dl_progress.configure(
            self.vid_ct_opt_frame,
            progress_color=f"{Config.theme["colors"]["error"]}",
            orientation="horizontal",
            width=250,
        )

    # delete the video frame and remove it from queue
    def delete_video(self) -> None:
        if not self.parent.is_downloading:
            self.parent.vid_queue.pop(self.index)
            self.vid_frame.destroy()
            self.parent.update_new_queue_clbck()
        else:
            Utils.create_dialog_error_notification("Unable to delete video")

    # Destorys widget
    def destory_video_widgets(self) -> None:
        self.vid_frame.destroy()

    # Adds video info to frame
    def append_vid_info(self) -> None:
        self.info = self.parent.get_vid_info()
        self.fetch_vid_thumbnail()
        self.create_vid_images()
        self.create_vid_widgets()
        self.config_vid_grid()
        self.append_vid_widget()
