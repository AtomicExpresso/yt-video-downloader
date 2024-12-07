from utils.config import Config
import customtkinter as ctk

#Handles app frames
class AppFrames:
  def __init__(self, parent):
    self.parent = parent
    self.main_frame = None
    self.progress_frame = None
    self.top_frame = None
    self.bottom_frame = None
  
  #Configures grid
  def grid_config(self):
    self.top_frame.grid_columnconfigure(0, weight=1)
    self.top_frame.grid_columnconfigure(1, weight=0)
    self.top_frame.grid_columnconfigure(2, weight=0)

    self.main_frame.grid_columnconfigure(0, weight=0)
    self.main_frame.grid_columnconfigure(1, weight=1)
    self.main_frame.grid_columnconfigure(2, weight=1)

    self.progress_frame.grid_rowconfigure(0, weight=0)
    self.progress_frame.grid_rowconfigure(1, weight=0)

    self.progress_frame.grid_columnconfigure(0, weight=0)
    self.progress_frame.grid_columnconfigure(1, weight=1)

    self.bottom_frame.grid_columnconfigure(0, weight=0)
    self.bottom_frame.grid_columnconfigure(1, weight=1)
    self.bottom_frame.grid_columnconfigure(2, weight=1)

  #re-creates frames, incase they need to be cleared
  def create_main_frame(self):
    self.main_frame = ctk.CTkScrollableFrame(
      self.parent, 
      corner_radius=0, 
      fg_color="#363636",
      scrollbar_button_color=f"{Config.primary_color}",
      scrollbar_button_hover_color=f"{Config.secondary_color}")
  def create_top_frame(self):
    self.top_frame = ctk.CTkFrame(
      self.parent, 
      fg_color=f"{Config.primary_color}", 
      corner_radius=0)
  def create_progress_frame(self):
    self.progress_frame = ctk.CTkFrame(
      self.parent,
      bg_color=f"{Config.primary_color}",
      fg_color="transparent",
      height=30, 
      corner_radius=0)
  def create_bottom_frame(self):
    self.bottom_frame = ctk.CTkFrame(
      self.parent, 
      fg_color=f"{Config.primary_color}",
      corner_radius=0)

  def create_frames(self):
    #Frame for url input
    self.create_top_frame()
    #Frame for main content
    self.create_main_frame()
    #Frame for progress bar
    self.create_progress_frame()
    #Frame for bottom row
    self.create_bottom_frame()