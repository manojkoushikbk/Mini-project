import tkinter as tk
from tkinter import ttk

class AdvertisementPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Advertisement Scrolling Panel")
        self.root.geometry("500x200")
        self.root.configure(bg="black")

        # Advertisement Input Field
        self.label = tk.Label(root, text="Enter Advertisement Text:", fg="white", bg="black")
        self.label.pack(pady=5)
        
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(root, text="Start Scrolling", command=self.start_scrolling, bg="green", fg="white")
        self.start_button.pack(pady=5)

        # Scrollable Label
        self.scroll_canvas = tk.Canvas(root, height=50, bg="black", highlightthickness=0)
        self.scroll_canvas.pack(fill="both", expand=True, pady=10)

        self.text_id = self.scroll_canvas.create_text(500, 25, text="", font=("Arial", 20, "bold"), fill="yellow", anchor="w")
        self.scroll_speed = 10  # Speed of scrolling (lower is faster)
    
    def start_scrolling(self):
        text = self.entry.get()
        if text:
            self.scroll_canvas.itemconfig(self.text_id, text=text)
            self.animate_text()

    def animate_text(self):
        x1, y1, x2, y2 = self.scroll_canvas.bbox(self.text_id)
        if x2 < 0:  # If text completely moves out, reset position
            self.scroll_canvas.coords(self.text_id, 500, 25)
        else:
            self.scroll_canvas.move(self.text_id, -2, 0)  # Move text left

        self.root.after(self.scroll_speed, self.animate_text)  # Repeat animation

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvertisementPanel(root)
    root.mainloop()
