import tkinter as tk
from .widget import Widget 
from math import sin, cos, radians


class Gauge(Widget):
    def __init__(self, parent, data, style):
        super().__init__(parent)
        self.data = data
        self.style = style
        self.needle_id = None
        self.value_text_id = None
        # Set initial value to 0
        self.value = 0;


    def draw(self):
        self.canvas = tk.Canvas(self, width=self.style["size"]["canvas_width"], height=self.style["size"]["canvas_width"], bg=self.style["color"]["canvas"])
        # Add canvas to frame and add frame to parent frame
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.pack()
        # Make sure canvas size is set before drawing
        self.update_idletasks()

        min_value = self.data["min_value"]
        max_value = self.data["max_value"]
        value = self.value
        size = self.style["size"]
        color = self.style["color"]
        start_angle = self.style.get("size", {}).get("start_angle", -135)
        end_angle = self.style.get("size", {}).get("end_angle", 135)
        canvas_size = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        tick_length_ratio = size.get("tick_length_ratio", 0.05)
        number_labels_ratio = size.get("number_labels_ratio", 0.05)
        number_label_offset_ratio = size.get("number_label_offset_ratio", 0.15)
        label_font_size_ratio = size.get("label_font_size_ratio", 0.05)
        value_font_size_ratio = size.get("value_font_size_ratio", 0.1)

        # Calculate size values based on the canvas size and displayed values
        value_range = max_value - min_value
        tick_length = canvas_size * tick_length_ratio
        number_labels = round(value_range * number_labels_ratio)
        number_label_offset = canvas_size * number_label_offset_ratio
        label_font_size = canvas_size * label_font_size_ratio
        value_font_size = canvas_size * value_font_size_ratio

        angle_range = end_angle - start_angle
        angle = start_angle + (value - min_value) / value_range * angle_range
        radius = canvas_size // 2 - 10
        needle_length = radius - number_label_offset - 10
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2

        # Draw gauge arc
        self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                               start=start_angle + 90, extent=angle_range,
                               style="arc", width=10, outline=color["gauge_arc"])

        # Draw tick marks
        num_ticks = number_labels + 1
        tick_angle_range = angle_range / num_ticks
        for i in range(num_ticks):
            tick_angle = start_angle + i * tick_angle_range
            tick_x1 = cx + (radius - tick_length) * sin(radians(tick_angle))
            tick_y1 = cy - (radius - tick_length) * cos(radians(tick_angle))
            tick_x2 = cx + radius * sin(radians(tick_angle))
            tick_y2 = cy - radius * cos(radians(tick_angle))
            if i % (num_ticks // (number_labels + 1)) == 0:  # Tick for number label
                self.canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill=color["ticks"], width=5)
            else:  # Regular tick mark
                tick_length_ratio = 1 - (i % (num_ticks // (number_labels + 1))) / (num_ticks // (number_labels + 1))
                self.canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill=color["ticks"], width=1 + tick_length_ratio * 2)

        # Draw number labels
        value_interval = value_range / number_labels
        for i in range(number_labels + 1):
            tick_value = min_value + i * value_interval
            tick_angle = start_angle + (tick_value - min_value) / value_range * angle_range
            tick_x = cx + (radius - number_label_offset) * sin(radians(tick_angle))
            tick_y = cy - (radius - number_label_offset) * cos(radians(tick_angle))
            self.canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill=color["number_label"], font=("Arial Black", int(label_font_size)))

        # Draw needle
        needle_x = cx + (radius - needle_length) * sin(radians(angle))
        needle_y = cy - (radius - needle_length) * cos(radians(angle))
        self.needle_id = self.canvas.create_line(cx, cy, needle_x, needle_y, fill=color["needle"], width=3)

        # Draw value box
        value_text = str(self.value)
        font = ('Arial Black', int(value_font_size))
        text_width = self.canvas.bbox(self.canvas.create_text(0, 0, text=value_text, font=font))[2]
        box_width = text_width + 10  # Add some padding
        x1 = cx - box_width / 2
        y1 = cy + radius / 2
        x2 = x1 + box_width
        y2 = y1 + value_font_size
        value_x = cx
        value_y = y1 + value_font_size / 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')
        self.value_text_id = self.canvas.create_text(value_x, value_y, text=value_text, font=font) 

    def update(self, value):
        self.value = value
        angle = -135 + ((value - self.value) / (self.data["max_value"] - self.data["min_value"])) * 270
        self.canvas.itemconfigure(self.needle_id, angle=angle)
        self.canvas.itemconfigure(self.value_text_id, text=str(value))

    def get_type(self):
        return {
            'widget_type': "gauge",
            'data_type': self.data["name"]
        }