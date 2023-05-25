import tkinter as tk
from math import sin, cos, radians


class GaugeWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.data_config = None
        self.style_config = None
        self.needle_id = None
        self.value_text_id = None
        self.canvas = None
        # Set initial value to 0
        self.value = 0;


    def draw_gauge(self, data_config, style_config):
        self.data_config = data_config
        self.style_config = style_config
        self.canvas = tk.Canvas(self, width=style_config["size"]["canvas_size"], height=style_config["size"]["canvas_size"], bg=style_config["color_scheme"]["background"])
        self.canvas.pack()  # Pack the canvas to make it visible
        self.update_idletasks()  # Update the window and its widgets

        min_value = data_config["min_value"]
        max_value = data_config["max_value"]
        value = self.value
        size_config = style_config["size"]
        color_config = style_config["color_scheme"]
        start_angle = style_config.get("size", {}).get("start_angle", -135)
        end_angle = style_config.get("size", {}).get("end_angle", 135)
        tick_length = size_config.get("tick_length", 10)
        number_ticks = size_config["number_ticks"]
        number_labels = size_config["number_labels"]
        number_label_offset = size_config.get("number_label_offset", tick_length + 10)
        value_font_size = size_config.get("value_font_size", 16)
        angle_range = end_angle - start_angle
        value_range = max_value - min_value
        angle = start_angle + (value - min_value) / value_range * angle_range
        radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 10
        needle_length = radius - number_label_offset - 10;
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2

        # Draw gauge arc
        self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                               start=start_angle + 90, extent=angle_range,
                               style="arc", width=10, outline=color_config["gauge_arc"])

        # Draw tick marks
        num_ticks = number_ticks
        tick_angle_range = angle_range / num_ticks
        for i in range(num_ticks + 1):
            tick_angle = start_angle + i * tick_angle_range
            tick_x1 = cx + (radius - tick_length) * sin(radians(tick_angle))
            tick_y1 = cy - (radius - tick_length) * cos(radians(tick_angle))
            tick_x2 = cx + radius * sin(radians(tick_angle))
            tick_y2 = cy - radius * cos(radians(tick_angle))
            self.canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill=color_config["ticks"], width=2)

        # Draw numbers
        value_interval = value_range / number_labels
        for i in range(number_labels + 1):
            tick_value = min_value + i * value_interval
            tick_angle = start_angle + (tick_value - min_value) / value_range * angle_range
            tick_x = cx + (radius - number_label_offset) * sin(radians(tick_angle))
            tick_y = cy - (radius - number_label_offset) * cos(radians(tick_angle))
            self.canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill=color_config["number_label"], font=("Arial Black", 12))

        # Draw needle
        needle_x = cx + (radius - needle_length) * sin(radians(angle))
        needle_y = cy - (radius - needle_length) * cos(radians(angle))
        self.needle_id = self.canvas.create_line(cx, cy, needle_x, needle_y, fill=color_config["needle"], width=3)

        # Draw value box
        # Calculate the size of the value box based on the font size and character length
        value_text = str(self.value)
        font = ('Arial Black', value_font_size)
        text_width = self.canvas.bbox(self.canvas.create_text(0, 0, text=value_text, font=font))[2]
        box_width = text_width + 10  # Add some padding
        # Draw a rectangle as the value box
        # Calculate coordinates for value box and value text
        x1 = cx - box_width / 2
        y1 = cy + radius / 2
        x2 = x1 + box_width
        y2 = y1 + value_font_size
        value_x = cx
        value_y = y1 + value_font_size / 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')
        # Draw the value text inside the box
        self.value_text_id = self.canvas.create_text(value_x, value_y, text=value_text, font=font)

    def update_gauge(self, value):
        self.value = value
        # Update the needle based on the new value
        angle = -135 + ((value - self.value) / (self.data_config["max_value"] - self.data_config["min_value"])) * 270
        self.canvas.itemconfigure(self.needle_id, angle=angle)
        # Update the value text with the new value
        self.canvas.itemconfigure(self.value_label_id, text=str(value))
    
    def get_type(self):
        return self.data_config["name"]