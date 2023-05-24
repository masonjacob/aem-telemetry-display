import json
from tkinter import *
from tkinter.ttk import *
import random

# Class imports
from widgets.gauge_widget import GaugeWidget
from widgets.bar_widget import BarWidget


class Application(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.gauge_widget = GaugeWidget(self.parent)
        self.bar_widget = BarWidget(self.parent)
        self.data_config = {}
        self.styles_config = {}

    def load_data_config(self, filename):
        with open(filename, 'r') as file:
            self.data_config = json.load(file)

    def load_styles_config(self, filename):
        with open(filename, 'r') as file:
            self.styles_config = json.load(file)

    def create_menu(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # Define the gauges menu
        gauges_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Gauges', menu=gauges_menu)
        self.parent.bind('<Button-1>', lambda event: self.select_gauge(list(self.data_config.keys())[0]))
        self.parent.bind('<Button-3>', lambda event: gauges_menu.post(event.x_root, event.y_root))

        # Define the bars menu
        bars_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Bars', menu=bars_menu)
        self.parent.bind('<Button-1>', lambda event: self.select_bar(list(self.data_config.keys())[0]), add='+')
        self.parent.bind('<Button-3>', lambda event: bars_menu.post(event.x_root, event.y_root), add='+')

        # Populate the gauges menu
        for data_type in self.data_config:
            gauges_menu.add_command(label=data_type, command=lambda x=data_type: self.select_gauge(x))

        # Populate the bars menu
        for data_type in self.data_config:
            bars_menu.add_command(label=data_type, command=lambda x=data_type: self.select_bar(x))

    def select_gauge(self, selection):
        self.gauge_widget.canvas.delete("all")  # Clear the canvas

        if selection in self.data_config:
            gauge_data = self.data_config[selection]

            if selection in self.styles_config["gauge_styles"]:
                gauge_styles = self.styles_config["gauge_styles"][selection]
            else:
                gauge_styles = self.styles_config["gauge_styles"]["default"]

            value = random.uniform(gauge_data["min_value"], gauge_data["max_value"])
            min_value = gauge_data["min_value"]
            max_value = gauge_data["max_value"]
            start_angle = gauge_styles.get("start_angle", -135)
            end_angle = gauge_styles.get("end_angle", 135)

            size_config = gauge_styles["size"]
            color_config = gauge_styles["color_scheme"]

            self.gauge_widget.draw_gauge(value, min_value, max_value, start_angle, end_angle, size_config, color_config)
            self.gauge_widget.pack()

    def select_bar(self, selection):
        self.bar_widget.canvas.delete("all")  # Clear the canvas

        if selection in self.data_config:
            bar_data = self.data_config[selection]

            if selection in self.styles_config["bar_styles"]:
                bar_styles = self.styles_config["bar_styles"][selection]
            else:
                bar_styles = self.styles_config["bar_styles"]["default"]

            value = random.uniform(bar_data["min_value"], bar_data["max_value"])
            min_value = bar_data["min_value"]
            max_value = bar_data["max_value"]
            bar_width = bar_styles["size"]["bar_width"]
            bar_height = bar_styles["size"]["bar_height"]

            color_config = bar_styles["color_scheme"]

            self.bar_widget.draw_bar(value, min_value, max_value, bar_width, bar_height, color_config)
            self.bar_widget.pack()

    def run(self):
        self.create_menu()
        self.select_gauge(list(self.data_config.keys())[0])
        self.parent.mainloop()


if __name__ == '__main__':
    root = Tk()
    root.geometry("600x500")
    root.title("Telemetry Display")

    app = Application(root)
    app.load_data_config("data_config.json")
    app.load_styles_config("styles_config.json")
    app.run()


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
