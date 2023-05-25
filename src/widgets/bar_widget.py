import tkinter as tk

class BarWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.data_config = None
        self.style_config = None
        self.bar_id = None
        self.value_text_id = None
        self.canvas = None
        # Set initial value to 0
        self.value = 0
    
    def draw_bar(self, data_config, style_config): 
        self.data_config = data_config
        self.style_config = style_config
        self.canvas = tk.Canvas(self, width=style_config["size"]["bar_width"] + 10, height=style_config["size"]["bar_height"] + 10, bg=style_config["color_scheme"]["background"])
        self.canvas.pack()  # Pack the canvas to make it visible
        self.update_idletasks()  # Update the window and its widgets

        min_value = data_config["min_value"]
        max_value = data_config["max_value"]
        value = self.value
        bar_width = style_config["size"]["bar_width"]
        bar_height = style_config["size"]["bar_height"]
        color_config = style_config["color_scheme"]

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

    def update_bar(self, value):
        self.value = value
        min_value = self.data_config["min_value"]
        max_value = self.data_config["max_value"]
        bar_width = self.styles_config["size"]["bar_width"]

        cx = self.canvas.winfo_width() // 2

        # Calculate bar length based on value
        value_range = max_value - min_value
        bar_length = (value - min_value) / value_range * bar_width

        # Update value bar
        self.canvas.itemconfigure(self.bar_id, x1= cx - bar_width // 2 + bar_length)

        # Update numerical value
        self.canvas.itemconfigure(self.value_text_id, text=str(value))
    
    def get_type(self):
        return self.data_config["name"]