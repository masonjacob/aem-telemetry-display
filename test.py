from tkinter import *
from tkinter.ttk import *
from math import sin, cos, radians
import json
import random

# Function to draw the gauge
def draw_gauge(canvas, config, value):
    min_value = config["min_value"]
    max_value = config["max_value"]
    start_angle = config["start_angle"]
    end_angle = config["end_angle"]

    angle_range = end_angle - start_angle
    value_range = max_value - min_value
    angle = start_angle + (value - min_value) / value_range * angle_range

    radius = min(canvas.winfo_width(), canvas.winfo_height()) // 2 - 10
    cx = canvas.winfo_width() // 2
    cy = canvas.winfo_height() // 2

    # Draw gauge arc
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                      start=start_angle, extent=angle_range,
                      style="arc", width=10, outline=config["arc_color"])

    # Draw tick marks
    num_ticks = config["num_ticks"]
    tick_angle_range = angle_range / num_ticks
    for i in range(num_ticks + 1):
        tick_angle = start_angle + i * tick_angle_range
        tick_x1 = cx + (radius - 10) * sin(radians(tick_angle))
        tick_y1 = cy - (radius - 10) * cos(radians(tick_angle))
        tick_x2 = cx + radius * sin(radians(tick_angle))
        tick_y2 = cy - radius * cos(radians(tick_angle))
        canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill=config["tick_color"], width=2)

    # Draw numbers
    num_values = config["num_values"]
    value_interval = value_range / num_values
    for i in range(num_values + 1):
        tick_value = min_value + i * value_interval
        tick_angle = start_angle + (tick_value - min_value) / value_range * angle_range
        tick_x = cx + (radius - 25) * sin(radians(tick_angle))
        tick_y = cy - (radius - 25) * cos(radians(tick_angle))
        canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill=config["number_color"],
                           font=("Arial", 12))

    # Draw needle
    needle_x = cx + (radius - 40) * sin(radians(angle))
    needle_y = cy - (radius - 40) * cos(radians(angle))
    canvas.create_line(cx, cy, needle_x, needle_y, fill=config["needle_color"], width=3)

    # Draw value box
    value_box_width = 80
    value_box_height = 30
    value_box_x = cx - value_box_width // 2
    value_box_y = cy + radius // 2 - value_box_height // 2
    canvas.create_rectangle(value_box_x, value_box_y, value_box_x + value_box_width, value_box_y + value_box_height,
                            fill=config["value_box_color"], outline="")
    canvas.create_text(cx, cy + radius // 2, text=str(int(value)), fill=config["value_color"], font=("Arial", 16))

# Function to handle gauge selection from the menu
def select_gauge(selection):
    canvas.delete("all")  # Clear the canvas

    with open('configs/gauges/data_config.json') as data_config_file:
        data_config = json.load(data_config_file)

    with open('configs/gauges/style_config.json') as style_config_file:
        style_config = json.load(style_config_file)

    config = data_config[selection]
    style = style_config[selection]

    icon_path = config["icon"]
    # Load and display icon
    icon = PhotoImage(file=icon_path)
    icon_label.configure(image=icon)
    icon_label.image = icon

    value = random.uniform(config["min_value"], config["max_value"])
    draw_gauge(canvas, style, value)

# Create the main window
root = Tk()
root.title('Gauge Display')

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create the "Gauges" menu
gauges_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Gauges', menu=gauges_menu)

# Load data configuration from file
with open('configs/gauges/data_config.json') as data_config_file:
    data_config = json.load(data_config_file)

# Populate the gauges menu from the data configuration
for gauge_name in data_config:
    gauges_menu.add_command(label=data_config[gauge_name]["name"], command=lambda name=gauge_name: select_gauge(name))

# Create the canvas for gauge display
canvas = Canvas(root, width=400, height=400, bg="#222")
canvas.pack(side=LEFT, padx=10)

# Create a label for displaying the icon
icon_label = Label(root)
icon_label.pack(side=LEFT, padx=10)

# Initially display the first gauge
select_gauge(list(data_config.keys())[0])

# Start the main event loop
root.mainloop()
