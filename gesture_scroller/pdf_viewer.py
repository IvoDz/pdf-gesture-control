import fitz
import tkinter as tk
from PIL import Image, ImageTk
from globals import gesture_queue, terminate
import queue

class PDFViewer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.current_page = 0
        self.a4_width_px = int(210 / 25.4 * 96) 
        self.a4_height_px = int(297 / 25.4 * 96)

        self.window = tk.Tk()
        self.window.title("PDF Viewer")
        self.window.geometry(f"{self.a4_width_px}x{self.a4_height_px}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)

        self.canvas = tk.Canvas(self.window, bg="white", width=self.a4_width_px, height=self.a4_height_px)
        self.canvas.pack(fill="both", expand=True)

        self.display_page(self.current_page)
        
        self.window.bind("<Left>", self.prev_page)
        self.window.bind("<Right>", self.next_page)
        self.window.bind("<Up>", self.next_page)
        self.window.bind("<Down>", self.prev_page)

    def display_page(self, page_num):
        self.canvas.delete("all")

        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(96 / 72, 96 / 72)) 
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(10, 10, image=self.photo, anchor="nw")

    def on_window_close(self):
        global terminate
        terminate.set()
        self.window.destroy()  
        
    def prev_page(self, event=None):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self, event=None):
        if self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def process_gesture(self, gesture: str):
        if gesture == "Open_Palm":
            self.next_page()
        elif gesture == "Closed_Fist":
            self.prev_page()
    
    def check_gesture(self):
        try:
            while not gesture_queue.empty() and not terminate.is_set():
                gesture = gesture_queue.get_nowait()
                print(f"Gesture detected: {gesture}")
                self.process_gesture(gesture)
        except queue.Empty:
            pass

    def run(self):
        while not terminate.is_set():  
            self.check_gesture()
            self.window.update()  