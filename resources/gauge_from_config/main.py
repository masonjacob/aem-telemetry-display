from tkinter import *
from tkinter.ttk import *
from math import sin, cos, radians
import random
import json


class GaugeWidget:
    def __init__(self, canvas):
        self.canvas = canvas
        self.value = None
        self.data_config = None
        self.start_angle = -135
        self.end_angle = 135

    def draw_gauge(self):
        if self.value is not None and self.data_config is not None:
            angle_range = self.end_angle - self.start_angle
            value_range = self.data_config['max_value'] - self.data_config['min_value']
            angle = self.start_angle + (self.value - self.data_config['min_value']) / value_range * angle_range

            radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 10
            cx = self.canvas.winfo_width() // 2
            cy = self.canvas.winfo_height() // 2

            # Draw gauge arc
            self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                                   start=self.start_angle + 90, extent=angle_range,
                                   style="arc", width=10, outline="#ddd")

            # Draw tick marks
            num_ticks = 30
            tick_angle_range = angle_range / num_ticks
            for i in range(num_ticks + 1):
                tick_angle = self.start_angle + i * tick_angle_range
                tick_x1 = cx + (radius - 10) * sin(radians(tick_angle))
                tick_y1 = cy - (radius - 10) * cos(radians(tick_angle))
                tick_x2 = cx + radius * sin(radians(tick_angle))
                tick_y2 = cy - radius * cos(radians(tick_angle))
                self.canvas.create_line(tick_x1, tick_y1, tick_x2, tick_y2, fill="#ddd", width=2)

            # Draw numbers
            num_values = 10
            value_range = self.data_config['max_value'] - self.data_config['min_value']
            value_interval = value_range / num_values
            for i in range(num_values + 1):
                tick_value = self.data_config['min_value'] + i * value_interval
                tick_angle = self.start_angle + (tick_value - self.data_config['min_value']) / value_range * angle_range
                tick_x = cx + (radius - 25) * sin(radians(tick_angle))
                tick_y = cy - (radius - 25) * cos(radians(tick_angle))
                self.canvas.create_text(tick_x, tick_y, text=str(int(tick_value)), fill="#ddd", font=("Arial", 12))

            # Draw needle
            needle_x = cx + (radius - 40) * sin(radians(angle))
            needle_y = cy - (radius - 40) * cos(radians(angle))
            self.canvas.create_line(cx, cy, needle_x, needle_y, fill="#f00", width=3)

            # Draw value box
            value_box_width = 80
            value_box_height = 30
            value_box_x = cx - value_box_width // 2
            value_box_y = cy + radius // 2 - value_box_height // 2
            self.canvas.create_rectangle(value_box_x, value_box_y, value_box_x + value_box_width,
                                         value_box_y + value_box_height,
                                         fill="#ddd", outline="")
            self.canvas.create_text(cx, cy + radius // 2, text=str(int(self.value)), fill="#f00", font=("Arial", 16))

    def set_value(self, value):
        self.value = value
        self.canvas.delete("all")
        self.draw_gauge()

    def set_data_config(self, data_config):
        self.data_config = data_config


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.data_config = None
        self.gauge_widget = None
        self.create_widgets()

    def create_widgets(self):
        # Create the menu bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # Create the "Gauges" menu
        gauges_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Gauges', menu=gauges_menu)

        # Read the data_config from file
        with open('data_config.json') as f:
            self.data_config = json.load(f)

        # Create menu items dynamically from the data_config
        for data_type in self.data_config:
            gauges_menu.add_command(label=data_type, command=lambda x=data_type: self.select_gauge(x))

        # Create the canvas for gauge display
        canvas = Canvas(self.master, width=400, height=400, bg="#222")
        canvas.pack()

        # Create the gauge widget
        self.gauge_widget = GaugeWidget(canvas)

    def select_gauge(self, selection):
        # Clear the canvas
        self.gauge_widget.set_data_config(self.data_config[selection])

        # Generate random value for testing
        value = random.uniform(self.data_config[selection]['min_value'], self.data_config[selection]['max_value'])
        self.gauge_widget.set_value(value)


# Create the main window
root = Tk()
root.title('Gauge Display')

# Create the application instance
app = Application(master=root)

# Start the main event loop
app.mainloop()



# class BarWidget:
#     def __init__(self, data_config):
#         self.data_config = data_config
#         self.value = None

#     def update(self, value):
#         self.value = value
#         # Update bar display based on the provided value
#         print(f"BarWidget: {self.data_config.name} - {self.value} {self.data_config.units}")

# class LayoutsWidget:
#     def __init__(self):
#         self.layouts = {}

#     def add_widget_to_layout(self, layout_name, widget):
#         if layout_name in self.layouts:
#             self.layouts[layout_name].append(widget)
#         else:
#             self.layouts[layout_name] = [widget]

#     def save_layout_preset(self, preset_name):
#         if preset_name not in self.layouts:
#             print("Error: Layout preset does not exist.")
#             return

#         with open(f"{preset_name}.json", "w") as preset_file:
#             widgets = [widget.data_config.name for widget in self.layouts[preset_name]]
#             json.dump(widgets, preset_file)
#         print(f"Layout preset '{preset_name}' saved.")

#     def load_layout_preset(self, preset_name):
#         try:
#             with open(f"{preset_name}.json", "r") as preset_file:
#                 widgets = json.load(preset_file)
#                 for widget_name in widgets:
#                     if widget_name in data_config:
#                         widget = GaugeWidget(data_config[widget_name])
#                         self.add_widget_to_layout(preset_name, widget)
#         except FileNotFoundError:
#             print(f"Error: Layout preset '{preset_name}' does not exist.")
#             return

#         print(f"Layout preset '{preset_name}' loaded.")

# class EditorWidget:
#     def __init__(self):
#         pass

#     def edit_gauge_style(self, gauge_widget):
#         # Edit the style of a gauge widget
#         print(f"Editing gauge style: {gauge_widget.data_config.name}")

#     def edit_data_config(self, data_config):
#         # Edit the configuration data
#         print(f"Editing data config: {data_config.name}")


# # Read data configuration from JSON file
# def read_data_config():
#     with open('data_config.json', 'r') as config_file:
#         data_config_json = json.load(config_file)
#         data_config = {}
#         for data_type, config in data_config_json.items():
#             data_config[data_type] = DataConfig(
#                 config['name'], config['units'], config['icon'],
#                 config['min_value'], config['max_value']
#             )
#         return data_config


# # # Example usage
# # data_config = read_data_config()

# # gauge_widget = GaugeWidget(data_config['RPM'])
# # bar_widget = BarWidget(data_config['Speed'])

# # layouts_widget = LayoutsWidget()
# # layouts_widget.add_widget_to_layout('Layout 1', gauge_widget)
# # layouts_widget.add_widget_to_layout('Layout 2', bar_widget)
# # layouts_widget.save_layout_preset('Preset 1')

# # editor_widget = EditorWidget()
# # editor_widget.edit_gauge_style(gauge_widget)
# # editor_widget.edit_data_config(data_config['RPM'])
