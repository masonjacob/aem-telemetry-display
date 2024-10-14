import tkinter as tk
from .widget import Widget
from .gauge import Gauge
from .bar import Bar

class Layout(Widget):
    def __init__(self, parent, config_manager, layout_name):
        super().__init__(parent)
        self.config_manager = config_manager
        self.layout_config = None
        self.data_config = self.config_manager.get_config("data_config")
        self.style_config = self.config_manager.get_config("style_config")
        self.widgets = []
        self.set_layout(layout_name)

    def draw(self):
        for widget in self.widgets:
            widget.draw(s)

        # Add frame to parent frame
        self.pack()

    # def erase(self):
    #     # super.erase()
    #     for widget in self.widgets:
    #         widget.erase()
    #     self.pack_forget()

    def set_layout(self, layout_name):
        self.layout_config = self.config_manager.get_config("layout_config")[layout_name]
        self.delete_widgets()
        self.add_widgets()
        self.draw()
        self.update_idletasks()

    def add_widgets(self):
        for widget_config in self.layout_config["widgets"]:
            widget_type = widget_config["widget_type"]
            if widget_type == "gauge":
                widget = Gauge(self, self.data_config[widget_config["data"]], self.style_config[widget_config["style"]])
            elif widget_type == "bar":
                widget = Bar(self, self.data_config[widget_config["data"]], self.style_config[widget_config["style"]])
            else:
                raise ValueError(f"Invalid widget type: {widget_type}")
            self.widgets.append(widget)

    def delete_widgets(self):
        for widget in self.widgets:
            self.widgets.remove(widget)
            widget.destroy()
