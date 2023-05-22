from tkinter import *
from tkinter.ttk import *
from math import sin, cos, radians
import random

# Function to draw the gauge
def draw_gauge(canvas, value, min_value, max_value, start_angle, end_angle):
    angle_range = end_angle - start_angle
    value_range = max_value - min_value
    angle = start_angle + (value - min_value) / value_range * angle_range

    radius = min(canvas.winfo_width(), canvas.winfo_height()) // 2 - 10
    cx = canvas.winfo_width() // 2
    cy = canvas.winfo_height() // 2

    # Draw gauge arc
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                      start=start_angle + 90, extent=angle_range,
                      style="arc", width=10, outline="#ddd")

    # Draw tick marks
    num_ticks = 30
    tick_angle_range = angle_range / num_ticks
    for i in range(num_ticks + 1):
        tick_angle = start_angle + i * tick_angle_range
        tick_x1 = cx + (radius - 10) * sin(radians(tick_angle))
        tick_y1 = cy - (radius - 10) * cos(radians(tick_angle))
        tick_x2 = cx + radius * sin(radians(tick_angle))
        tick_y2 = cy - radius * cos(radians(tick_angle))
        canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill="#ddd", width=2)

    # Draw numbers
    num_values = 10
    value_range = max_value - min_value
    value_interval = value_range / num_values
    for i in range(num_values + 1):
        tick_value = min_value + i * value_interval
        tick_angle = start_angle + (tick_value - min_value) / value_range * angle_range
        tick_x = cx + (radius - 25) * sin(radians(tick_angle))
        tick_y = cy - (radius - 25) * cos(radians(tick_angle))
        canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill="#ddd", font=("Arial", 12))

    # Draw needle
    needle_x = cx + (radius - 40) * sin(radians(angle))
    needle_y = cy - (radius - 40) * cos(radians(angle))
    canvas.create_line(cx, cy, needle_x, needle_y, fill="#f00", width=3)

     # Draw value box
    value_box_width = 80
    value_box_height = 30
    value_box_x = cx - value_box_width // 2
    value_box_y = cy + radius // 2 - value_box_height // 2
    canvas.create_rectangle(value_box_x, value_box_y, value_box_x + value_box_width, value_box_y + value_box_height,
                            fill="#ddd", outline="")
    canvas.create_text(cx, cy + radius // 2, text=str(int(value)), fill="#f00", font=("Arial", 16))

# Function to handle gauge selection from the menu
def select_gauge(selection):
    canvas.delete("all")  # Clear the canvas

    if selection == "Speed":
        value = random.uniform(0, 200)  # Test value for speed gauge
        min_value = 0
        max_value = 200
        start_angle = -135
        end_angle = 135
        draw_gauge(canvas, value, min_value, max_value, start_angle, end_angle)
    elif selection == "RPM":
        value = random.uniform(0, 8000)  # Test value for RPM gauge
        min_value = 0
        max_value = 8000
        start_angle = -135
        end_angle = 135
        draw_gauge(canvas, value, min_value, max_value, start_angle, end_angle)

# Create the main window
root = Tk()
root.title('Gauge Display')

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create the "Gauges" menu
gauges_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Gauges', menu=gauges_menu)
gauges_menu.add_command(label='Speed', command=lambda: select_gauge("Speed"))
gauges_menu.add_command(label='RPM', command=lambda: select_gauge("RPM"))

# Create the canvas for gauge display
canvas = Canvas(root, width=400, height=400, bg="#222")
canvas.pack()

# Initially display the speed gauge
select_gauge("Speed")

# Start the main event loop
mainloop()
