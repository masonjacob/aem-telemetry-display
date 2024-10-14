import tkinter as tk

class Widget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.canvas = None

    def draw(self):
        raise NotImplementedError("Subclasses must implement the draw() method.")

    # def erase(self):
    #     print("erasing widget: ", self)
    #     self.pack_forget()  # Hide the widget
    #     if self.canvas is not None:
    #         self.canvas.destroy()  # Remove the canvas
    #     self.destroy()
        
    
    def update(self, value):
        raise NotImplementedError("Subclasses must implement the update() method.")

    # def get_type(self):
    #     raise NotImplementedError("Subclasses must implement the get_type() method.")
