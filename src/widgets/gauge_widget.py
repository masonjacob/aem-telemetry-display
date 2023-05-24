import tkinter as tk
from math import sin, cos, radians


class GaugeWidget(tk.Frame):
    def __init__(self, parent, data_config, style_config):
        super().__init__(parent)
        self.parent = parent
        self.needle_id = None
        self.data_config = data_config
        self.style_config = style_config
        # Set initial value to the minimum
        self.value = data_config.get('min_value', 0)
        self.canvas = tk.Canvas(self, style_config["size"]["canvas-size"], style_config["size"]["canvas-size"], bg=style_config["color_scheme"]["background"])

    def draw_gauge(self):
        min_value = self.data_config["min_value"]
        max_value = self.data_config["max_value"]
        value = self.value
        color_config = self.style_config["color_scheme"]
        start_angle = self.style_config.get(["size"]["start_angle"], -135)
        end_angle = self.style_config.get(["size"]["end_angle"], 135)
        tick_length = size_config.get("tick_length", 10)
        number_ticks = size_config["number_ticks"]
        number_labels = size_config["number_labels"]
        number_label_offset = size_config.get("number_label_offset", tick_length + 10)
        needle_length = size_config["needle_length"]
        value_box_width = size_config["value_box_width"]
        value_box_height = size_config["value_box_height"]


        angle_range = end_angle - start_angle
        value_range = max_value - min_value
        angle = start_angle + (value - min_value) / value_range * angle_range

        radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 10
        

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


    # Calculate the size of the value box based on the font size and character length
        value_text = str(self.value)
        font = ('Arial', font_size)
        text_width = self.canvas.bbox(self.canvas.create_text(0, 0, text=value_text, font=font))[2]
        box_width = text_width + 10  # Add some padding

        # Example code: Draw a rectangle as the value box
        x1 = 200 - box_width / 2
        y1 = 200 - font_size / 2
        x2 = x1 + box_width
        y2 = y1 + font_size
        self.value_label_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')

        # Example code: Draw the value text inside the box
        self.canvas.create_text(200, 200, text=value_text, font=font)

    def update_needle(self, value):
        # Update the needle based on the new value
        # ...

        # Example code: Rotate the needle based on the value
        angle = -135 + ((value - self.value) / (max_value - min_value)) * 270
        self.canvas.itemconfigure(self.needle_id, angle=angle)

    def update_value_label(self, value):
        # Update the value label with the new value
        self.canvas.itemconfigure(self.value_label_id, text=str(value))
        self.value = value

    def set_value(self, value):
        self.value = value


    def update_gauge(self, value):
        angle = -135 + ((value - self.value) / (self.max_value - self.min_value)) * 270
        self.canvas.itemconfigure(self.needle_id, angle=angle)