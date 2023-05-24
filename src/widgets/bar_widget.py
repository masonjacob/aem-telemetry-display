import tkinter as tk

class BarWidget(tk.Frame):
    def __init__(self, parent, data_config, style_config):
        super().__init__(parent)
        self.parent = parent
        self.data_config = data_config
        self.style_config = style_config
        # Set initial value to the minimum
        self.value = data_config.get('min_value', 0)
        self.canvas = tk.Canvas(self, style_config["size"]["canvas-size"], style_config["size"]["canvas-size"], bg=style_config["color_scheme"]["background"])
    
    def draw_bar(self): 
        min_value = self.data_config["min_value"]
        max_value = self.data_config["max_value"]
        value = self.value
        bar_width = self.data_config["bar_width"]
        bar_height = self.data_config["bar_height"]
        color_config = self.style_config["color_scheme"]


        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2

        # Calculate bar length based on value
        value_range = max_value - min_value
        bar_length = (value - min_value) / value_range * bar_width

        # Draw background bar
        self.canvas.create_rectangle(cx - bar_width // 2, cy - bar_height // 2,
                                     cx + bar_width // 2, cy + bar_height // 2,
                                     fill=color_config["background"], outline="")

        # Draw value bar
        self.canvas.create_rectangle(cx - bar_width // 2, cy - bar_height // 2,
                                     cx - bar_width // 2 + bar_length, cy + bar_height // 2,
                                     fill=color_config["value_bar"], outline="")

        # Overlay numerical value
        self.canvas.create_text(cx, cy, text=str(int(value)), fill=color_config.get("value_text", "white"),
                                font=("Arial", 16))

