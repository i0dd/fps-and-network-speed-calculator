import tkinter as tk
from tkinter import StringVar
import psutil
import time
import threading
import mss
from PIL import Image

class overApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True)  
        self.root.geometry("+1300+10")  

        
        self.fps_text = StringVar()
        self.speed_text = StringVar()

        # Set up labels
        self.fps_label = tk.Label(root, textvariable=self.fps_text, font=("Helvetica", 16), fg="white", bg="black")
        self.fps_label.pack()
        self.speed_label = tk.Label(root, textvariable=self.speed_text, font=("Helvetica", 16), fg="white", bg="black")
        self.speed_label.pack()

        
        self.sct = mss.mss()

        # Initialize previous network stats
        self.prev_bytes_sent = psutil.net_io_counters().bytes_sent
        self.prev_bytes_recv = psutil.net_io_counters().bytes_recv

        
        self.update_fps()
        self.update_speed()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_fps(self):
        monitor = self.sct.monitors[1]
        start_time = time.time()
        sct_img = self.sct.grab(monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        self.fps_text.set(f"FPS: {fps:.2f}")

        # Schedule the next update
        self.root.after(1000, self.update_fps)

    def update_speed(self):
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        upload_speed = (bytes_sent - self.prev_bytes_sent) / 1024  #KB/s
        download_speed = (bytes_recv - self.prev_bytes_recv) / 1024  #KB/s

        self.prev_bytes_sent = bytes_sent
        self.prev_bytes_recv = bytes_recv

        speed_text = f"Speed: {upload_speed:.2f} KB/s Up, {download_speed:.2f} KB/s Down"
        self.speed_text.set(speed_text)

        
        self.root.after(1000, self.update_speed)

    def on_close(self):
        self.sct.close()
        self.root.destroy()


root = tk.Tk()
app = OverlayApp(root)


root.mainloop()

