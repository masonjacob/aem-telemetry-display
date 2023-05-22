from tkinter import *
from tkinter.ttk import *
from math import sin, cos, radians
import random
import json


class DataModel:
    def __init__(self, name, units, min_value, max_value):
        self.name = name
        self.units = units
        self.min_value = min_value
        self.max_value = max_value


class GaugeWidget:
    def __init__(self, canvas, data_model, style):
        self.canvas = canvas
        self.data_model = data_model
        self.style = style
        self.draw_gauge()

    def draw_gauge(self):
        value = random.uniform(self.data_model.min_value, self.data_model.max_value)
        min_value = self.data_model.min_value
        max_value = self.data_model.max_value
        start_angle = -135
        end_angle = 135

        # Clear the canvas
        self.canvas.delete("all")

        # Draw gauge arc
        radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 10
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2
        self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                               start=start_angle + 90, extent=end_angle - start_angle,
                               style="arc", width=10, outline=self.style['arc_color'])

        # Draw needle
        angle_range = end_angle - start_angle
        angle = start_angle + (value - min_value) / (max_value - min_value) * angle_range
        needle_x = cx + (radius - 40) * sin(radians(angle))
        needle_y = cy - (radius - 40) * cos(radians(angle))
        self.canvas.create_line(cx, cy, needle_x, needle_y, fill=self.style['needle_color'], width=3)

        # Draw value box
        value_box_width = 80
        value_box_height = 30
        value_box_x = cx - value_box_width // 2
        value_box_y = cy + radius // 2 - value_box_height // 2
        self.canvas.create_rectangle(value_box_x, value_box_y, value_box_x + value_box_width,
                                     value_box_y + value_box_height, fill=self.style['value_box_fill'], outline="")
        self.canvas.create_text(cx, cy + radius // 2, text=str(int(value)) + " " + self.data_model.units,
                                fill=self.style['value_color'], font=("Arial", 16))


class BarWidget:
    def __init__(self, canvas, data_model, style):
        self.canvas = canvas
        self.data_model = data_model
        self.style = style
        self.draw_bar()

    def draw_bar(self):
        value = random.uniform(self.data_model.min_value, self.data_model.max_value)
        min_value = self.data_model.min_value
        max_value = self.data_model.max_value

        # Clear the canvas
        self.canvas.delete("all")

        # Draw value bar
        bar_width = self.canvas.winfo_width() - 20
        bar_height = 20
        bar_x = 10
        bar_y = self.canvas.winfo_height() // 2 - bar_height // 2
        fill_width = (value - min_value) / (max_value - min_value) * bar_width
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + fill_width, bar_y + bar_height,
                                     fill=self.style['fill_color'], outline="")
        self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                     fill=self.style['bar_fill'], outline="", width=2)

        # Draw value text
        value_x = bar_x + fill_width + 10
        value_y = self.canvas.winfo_height() // 2
        self.canvas.create_text(value_x, value_y, text=str(int(value)) + " " + self.data_model.units,
                                fill=self.style['value_color'], font=("Arial", 12))


class EditorWidget:
    def __init__(self, root):
        self.root = root
        self.data_config = []
        self.gauge_styles = {}
        self.bar_styles = {}
        self.layouts = {}
        self.load_config_files()

    def load_config_files(self):
        try:
            with open('data_config.json', 'r') as file:
                self.data_config = json.load(file)

            with open('gauge_styles.json', 'r') as file:
                self.gauge_styles = json.load(file)

            with open('bar_styles.json', 'r') as file:
                self.bar_styles = json.load(file)

            with open('layouts.json', 'r') as file:
                self.layouts = json.load(file)

        except FileNotFoundError:
            print("Error: Configuration files not found.")

    def save_config_files(self):
        with open('data_config.json', 'w') as file:
            json.dump(self.data_config, file, indent=2)

        with open('gauge_styles.json', 'w') as file:
            json.dump(self.gauge_styles, file, indent=2)

        with open('bar_styles.json', 'w') as file:
            json.dump(self.bar_styles, file, indent=2)

        with open('layouts.json', 'w') as file:
            json.dump(self.layouts, file, indent=2)

    def create_editor(self):
        editor_window = Toplevel(self.root)
        editor_window.title("Widget Editor")

        # Create the Notebook widget to hold tabs
        notebook = Notebook(editor_window)
        notebook.pack()

        # Create the Data Config tab
        data_config_frame = Frame(notebook)
        notebook.add(data_config_frame, text="Data Config")
        self.create_data_config_editor(data_config_frame)

        # Create the Gauge Styles tab
        gauge_styles_frame = Frame(notebook)
        notebook.add(gauge_styles_frame, text="Gauge Styles")
        self.create_styles_editor(gauge_styles_frame, self.gauge_styles)

        # Create the Bar Styles tab
        bar_styles_frame = Frame(notebook)
        notebook.add(bar_styles_frame, text="Bar Styles")
        self.create_styles_editor(bar_styles_frame, self.bar_styles)

        # Create the Layouts tab
        layouts_frame = Frame(notebook)
        notebook.add(layouts_frame, text="Layouts")
        self.create_layouts_editor(layouts_frame)

        # Save button
        save_button = Button(editor_window, text="Save", command=self.save_config_files)
        save_button.pack()

    def create_data_config_editor(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        # Create the headers
        Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        Label(frame, text="Units").grid(row=0, column=1, padx=5, pady=5)
        Label(frame, text="Min Value").grid(row=0, column=2, padx=5, pady=5)
        Label(frame, text="Max Value").grid(row=0, column=3, padx=5, pady=5)
        Button(frame, text="Add", command=self.add_data_model).grid(row=0, column=4, padx=5, pady=5)

        # Create the data models
        for index, data_model in enumerate(self.data_config):
            Label(frame, text=data_model['name']).grid(row=index + 1, column=0, padx=5, pady=5)
            Label(frame, text=data_model['units']).grid(row=index + 1, column=1, padx=5, pady=5)
            Label(frame, text=str(data_model['min_value'])).grid(row=index + 1, column=2, padx=5, pady=5)
            Label(frame, text=str(data_model['max_value'])).grid(row=index + 1, column=3, padx=5, pady=5)
            Button(frame, text="Edit", command=lambda i=index: self.edit_data_model(i)).grid(row=index + 1, column=4, padx=5, pady=5)
            Button(frame, text="Delete", command=lambda i=index: self.delete_data_model(i)).grid(row=index + 1, column=5, padx=5, pady=5)

    def add_data_model(self):
        data_model = {
            "name": "New Data",
            "units": "Unit",
            "min_value": 0,
            "max_value": 100
        }
        self.data_config.append(data_model)
        self.create_editor()

    def edit_data_model(self, index):
        data_model = self.data_config[index]
        editor = Toplevel(self.root)
        editor.title("Edit Data Model")

        Label(editor, text="Name").grid(row=0, column=0, padx=5, pady=5)
        name_entry = Entry(editor)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, data_model['name'])

        Label(editor, text="Units").grid(row=1, column=0, padx=5, pady=5)
        units_entry = Entry(editor)
        units_entry.grid(row=1, column=1, padx=5, pady=5)
        units_entry.insert(0, data_model['units'])

        Label(editor, text="Min Value").grid(row=2, column=0, padx=5, pady=5)
        min_value_entry = Entry(editor)
        min_value_entry.grid(row=2, column=1, padx=5, pady=5)
        min_value_entry.insert(0, str(data_model['min_value']))

        Label(editor, text="Max Value").grid(row=3, column=0, padx=5, pady=5)
        max_value_entry = Entry(editor)
        max_value_entry.grid(row=3, column=1, padx=5, pady=5)
        max_value_entry.insert(0, str(data_model['max_value']))

        save_button = Button(editor, text="Save", command=lambda: self.save_data_model(index, name_entry.get(),
                                                                                     units_entry.get(),
                                                                                     min_value_entry.get(),
                                                                                     max_value_entry.get()))
        save_button.grid(row=4, columnspan=2, padx=5, pady=5)

    def save_data_model(self, index, name, units, min_value, max_value):
        self.data_config[index]['name'] = name
        self.data_config[index]['units'] = units
        self.data_config[index]['min_value'] = float(min_value)
        self.data_config[index]['max_value'] = float(max_value)
        self.create_editor()

    def delete_data_model(self, index):
        del self.data_config[index]
        self.create_editor()

    def create_styles_editor(self, frame, styles):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        # Create the headers
        Label(frame, text="Style").grid(row=0, column=0, padx=5, pady=5)
        Label(frame, text="Arc Color").grid(row=0, column=1, padx=5, pady=5)
        Label(frame, text="Needle Color").grid(row=0, column=2, padx=5, pady=5)
        Label(frame, text="Value Box Fill").grid(row=0, column=3, padx=5, pady=5)
        Label(frame, text="Value Color").grid(row=0, column=4, padx=5, pady=5)
        Button(frame, text="Add", command=lambda: self.add_style(frame, styles)).grid(row=0, column=5, padx=5, pady=5)

        # Create the styles
        row = 1
        for style_name, style in styles.items():
            Label(frame, text=style_name).grid(row=row, column=0, padx=5, pady=5)
            Entry(frame, textvariable=StringVar(frame, value=style.get('arc_color', ''))).grid(row=row, column=1, padx=5, pady=5)
            Entry(frame, textvariable=StringVar(frame, value=style.get('needle_color', ''))).grid(row=row, column=2, padx=5, pady=5)
            Entry(frame, textvariable=StringVar(frame, value=style.get('value_box_fill', ''))).grid(row=row, column=3, padx=5, pady=5)
            Entry(frame, textvariable=StringVar(frame, value=style.get('value_color', ''))).grid(row=row, column=4, padx=5, pady=5)
            Button(frame, text="Edit", command=lambda i=style_name: self.edit_style(frame, styles, i)).grid(row=row, column=5, padx=5, pady=5)
            Button(frame, text="Delete", command=lambda i=style_name: self.delete_style(frame, styles, i)).grid(row=row, column=6, padx=5, pady=5)
            row += 1

    def add_style(self, frame, styles):
        style_name = "New Style"
        styles[style_name] = {
            "arc_color": "#ddd",
            "needle_color": "#f00",
            "value_box_fill": "#ddd",
            "value_color": "#f00"
        }
        self.create_editor()

    def edit_style(self, frame, styles, style_name):
        style = styles[style_name]
        editor = Toplevel(self.root)
        editor.title("Edit Style: " + style_name)

        Label(editor, text="Arc Color").grid(row=0, column=0, padx=5, pady=5)
        arc_color_entry = Entry(editor)
        arc_color_entry.grid(row=0, column=1, padx=5, pady=5)
        arc_color_entry.insert(0, style['arc_color'])

        Label(editor, text="Needle Color").grid(row=1, column=0, padx=5, pady=5)
        needle_color_entry = Entry(editor)
        needle_color_entry.grid(row=1, column=1, padx=5, pady=5)
        needle_color_entry.insert(0, style['needle_color'])

        Label(editor, text="Value Box Fill").grid(row=2, column=0, padx=5, pady=5)
        value_box_fill_entry = Entry(editor)
        value_box_fill_entry.grid(row=2, column=1, padx=5, pady=5)
        value_box_fill_entry.insert(0, style['value_box_fill'])

        Label(editor, text="Value Color").grid(row=3, column=0, padx=5, pady=5)
        value_color_entry = Entry(editor)
        value_color_entry.grid(row=3, column=1, padx=5, pady=5)
        value_color_entry.insert(0, style['value_color'])

        save_button = Button(editor, text="Save", command=lambda: self.save_style(styles, style_name,
                                                                                 arc_color_entry.get(),
                                                                                 needle_color_entry.get(),
                                                                                 value_box_fill_entry.get(),
                                                                                 value_color_entry.get()))
        save_button.grid(row=4, columnspan=2, padx=5, pady=5)

    def save_style(self, styles, style_name, arc_color, needle_color, value_box_fill, value_color):
        style = styles[style_name]
        style['arc_color'] = arc_color
        style['needle_color'] = needle_color
        style['value_box_fill'] = value_box_fill
        style['value_color'] = value_color
        self.create_editor()

    def delete_style(self, frame, styles, style_name):
        del styles[style_name]
        self.create_editor()

    def create_layouts_editor(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        # Create the headers
        Label(frame, text="Layout").grid(row=0, column=0, padx=5, pady=5)
        Label(frame, text="Widgets").grid(row=0, column=1, padx=5, pady=5)
        Button(frame, text="Add", command=lambda: self.add_layout(frame)).grid(row=0, column=2, padx=5, pady=5)

        # Create the layouts
        row = 1
        for layout in self.layouts:
            if isinstance(layout, dict):
                layout_name = layout['name']
                layout_widgets = layout['widgets']
            else:
                layout_name = layout
                layout_widgets = []
            Label(frame, text=layout_name).grid(row=row, column=0, padx=5, pady=5)
            Label(frame, text=", ".join(layout_widgets)).grid(row=row, column=1, padx=5, pady=5)
            Button(frame, text="Edit", command=lambda i=layout_name: self.edit_layout(frame, i)).grid(row=row, column=2, padx=5, pady=5)
            Button(frame, text="Delete", command=lambda i=layout_name: self.delete_layout(frame, i)).grid(row=row, column=3, padx=5, pady=5)
            row += 1

    def add_layout(self, frame):
        layout_name = "New Layout"
        self.layouts[layout_name] = {"widgets": []}
        self.create_editor()

    def edit_layout(self, frame, layout_name):
        layout = self.layouts[layout_name]
        editor = Toplevel(self.root)
        editor.title("Edit Layout: " + layout_name)

        widgets_frame = Frame(editor)
        widgets_frame.pack()

        available_widgets = list(self.data_config)
        available_widgets.extend(list(self.gauge_styles))
        available_widgets.extend(list(self.bar_styles))

        for index, widget in enumerate(available_widgets):
            var = IntVar(value=0)
            if widget in layout['widgets']:
                var.set(1)
            Checkbutton(widgets_frame, text=widget, variable=var).grid(row=index // 4, column=index % 4, padx=5, pady=5)

        save_button = Button(editor, text="Save", command=lambda: self.save_layout(layout, widgets_frame))
        save_button.pack()

    def save_layout(self, layout, widgets_frame):
        layout['widgets'] = [widget.cget('text') for widget in widgets_frame.winfo_children() if widget.cget('variable').get() == 1]
        self.create_editor()

    def delete_layout(self, frame, layout_name):
        del self.layouts[layout_name]
        self.create_editor()


# Create the main window
root = Tk()
root.title("Widget Editor")

# Create the editor widget
editor_widget = EditorWidget(root)
editor_widget.create_editor()

# Start the main event loop
root.mainloop()
