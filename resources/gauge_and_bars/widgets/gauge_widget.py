import tkinter as tk
from math import sin, cos, radians


class GaugeWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, width=400, height=400, bg="#222")
        self.canvas.pack()

    def draw_gauge(self, value, min_value, max_value, start_angle, end_angle, size_config, color_config):
        angle_range = end_angle - start_angle
        value_range = max_value - min_value
        angle = start_angle + (value - min_value) / value_range * angle_range
        
        #self.canvas = Canvas(self, width=size_config["canvas_size"], height=size_config["canvas_size"], bg=color_config["background"])
        radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 10
        tick_length = size_config.get("tick_length", 10)
        number_ticks = size_config["number_ticks"]
        number_labels = size_config["number_labels"]
        number_label_offset = size_config.get("number_label_offset", tick_length + 10)
        needle_length = size_config["needle_length"]
        value_box_width = size_config["value_box_width"]
        value_box_height = size_config["value_box_height"]

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
            self.canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill=color_config["number_label"], font=("Arial", 12))

        # Draw needle
        needle_x = cx + (radius - needle_length) * sin(radians(angle))
        needle_y = cy - (radius - needle_length) * cos(radians(angle))
        self.canvas.create_line(cx, cy, needle_x, needle_y, fill=color_config["needle"], width=3)

        # Draw value box
        value_box_x = cx - value_box_width // 2
        value_box_y = cy + radius // 2 - value_box_height // 2
        self.canvas.create_rectangle(value_box_x, value_box_y, value_box_x + value_box_width,
                                     value_box_y + value_box_height,
                                     fill=color_config["value_box"], outline="")
        self.canvas.create_text(cx, cy + radius // 2, text=str(int(value)), fill=color_config["value"], font=("Arial", 16))
