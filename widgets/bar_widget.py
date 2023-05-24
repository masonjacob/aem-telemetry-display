import tkinter as tk

class BarWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, width=400, height=400, bg="#222")
        self.canvas.pack()

    def draw_bar(self, value, min_value, max_value, bar_width, bar_height, color_config):
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
