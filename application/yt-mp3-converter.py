import yt_dlp
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import re
import requests
import os
import subprocess

def download():
    link = link_entry.get()
    filename = filename_entry.get()
    if not link:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': r'C:\Users\joshj\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin',
        'outtmpl': (filename if filename else '%(title)s') + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([link])
        # Determine the output file name
        output_file = (filename if filename else get_title_from_url(link)) + '.mp3'
        abs_path = os.path.abspath(output_file)
        downloaded_label.config(text=f"Downloaded: {output_file}")
        open_button.config(state=tk.NORMAL)
        open_button.file_path = abs_path
        messagebox.showinfo("Success", "Download complete! The audio has been saved as an MP3 file.")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading: {e}")
        open_button.config(state=tk.DISABLED)
        open_button.file_path = None

# Helper to get video title if no filename is given
def get_title_from_url(url):
    try:
        resp = requests.get(url)
        title = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE)
        if title:
            return title.group(1).replace(' - YouTube', '').strip()
    except Exception:
        pass
    return 'output'

def open_file_location():
    file_path = getattr(open_button, 'file_path', None)
    if file_path and os.path.exists(file_path):
        # Open folder and select the file
        subprocess.run(f'explorer /select,"{file_path}"')
    else:
        messagebox.showerror("Error", "File not found.")

root = tk.Tk()
root.title("YouTube to MP3 Converter")
root.configure(bg='#2c3e50')
root.geometry('500x250')
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', background='#e74c3c', foreground='white', font=('Arial', 11, 'bold'))
style.map('TButton', background=[('active', '#c0392b')])
style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
style.configure('TEntry', fieldbackground='white', foreground='#2c3e50', font=('Arial', 10))

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="YouTube Link:").grid(row=0, column=0, sticky='w', pady=5)
link_entry = ttk.Entry(frame, width=50)
link_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Filename (optional):").grid(row=1, column=0, sticky='w', pady=5)
filename_entry = ttk.Entry(frame, width=50)
filename_entry.grid(row=1, column=1, pady=5)

ttk.Button(frame, text="Download MP3", command=download).grid(row=2, column=0, columnspan=2, pady=15)

downloaded_label = ttk.Label(frame, text="", foreground="#2ecc71", font=("Arial", 10, "bold"))
downloaded_label.grid(row=3, column=0, columnspan=2, pady=5)

open_button = ttk.Button(frame, text="Open File Location", command=open_file_location, state=tk.DISABLED)
open_button.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()