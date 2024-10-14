import tkinter as tk
from .widget import Widget

class Bar(Widget):
    def __init__(self, parent, data, style):
        super().__init__(parent)
        self.data = data
        self.style = style
        self.bar_id = None
        self.value_text_id = None
        # Set initial value to 0
        self.value = 0
    
    def draw(self): 
        bar_height_ratio = self.style.get("bar_height_ratio", 0.1)
        self.canvas = tk.Canvas(self, width=self.style["size"]["canvas_width"], height=self.style["size"]["canvas_width"] * bar_height_ratio, bg=self.style["color"]["canvas"])
        # Add canvas to frame and add frame to parent frame
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.pack()
        # Make sure canvas size is set before drawing
        self.update_idletasks()

        min_value = self.data["min_value"]
        max_value = self.data["max_value"]
        value = self.value
        bar_width = self.style["size"]["canvas_width"] - 10
        bar_height = (self.style["size"]["canvas_width"] * bar_height_ratio)  - 10
        color_config = self.style["color"]

        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2

        # Calculate bar length based on value
        value_range = max_value - min_value
        bar_length = (value - min_value) / value_range * bar_width

        # Draw background bar
        self.canvas.create_rectangle(cx - bar_width // 2, cy - bar_height // 2,
                                     cx + bar_width // 2, cy + bar_height // 2,
                                     fill=color_config["background_bar"], outline="")

        # Draw value bar
        self.bar_id = self.canvas.create_rectangle(cx - bar_width // 2, cy - bar_height // 2,
                                     cx - bar_width // 2 + bar_length, cy + bar_height // 2,
                                     fill=color_config["value_bar"], outline="")

        # Overlay numerical value
        self.value_text_id = self.canvas.create_text(cx, cy, text=str(value), fill=color_config.get("value_text", "white"),
                                font=("Arial Black", 16))
        

    def update(self, value):
        self.value = value
        min_value = self.data["min_value"]
        max_value = self.data["max_value"]
        bar_width = self.style["size"]["canvas_width"] - 10

        cx = self.canvas.winfo_width() // 2

        # Calculate bar length based on value
        value_range = max_value - min_value
        bar_length = (value - min_value) / value_range * bar_width

        # Update value bar
        self.canvas.itemconfigure(self.bar_id, x1= cx - bar_width // 2 + bar_length)

        # Update numerical value
        self.canvas.itemconfigure(self.value_text_id, text=str(value))
    
    def get_type(self):
        return {
            'widget_type': "bar",
            'data_type': self.data["name"]
        }