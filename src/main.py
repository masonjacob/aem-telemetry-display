import json
from tkinter import *
from tkinter.ttk import *
import serial
import os
import threading


# Class imports
from widgets.gauge_widget import GaugeWidget
from widgets.bar_widget import BarWidget


class Application(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config_path = "configs"
        self.gauge_widget = GaugeWidget(self.parent)
        self.bar_widget = BarWidget(self.parent)
        self.data_config = {}
        self.styles_config = {}
        self.serial_config = {}
        self.serial_port = None
        self.serial_thread = None

    def load_data_config(self, filename):
        file_path = os.path.join(self.config_path, filename)
        with open(file_path, 'r') as file:
            self.data_config = json.load(file)

    def load_styles_config(self, filename):
        file_path = os.path.join(self.config_path, filename)
        with open(file_path, 'r') as file:
            self.styles_config = json.load(file)
    
    def load_serial_config(self, filename):
        file_path = os.path.join(self.config_path, filename)
        with open(file_path, 'r') as file:
            self.serial_config = json.load(file)

    def create_menu(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # Define the gauges menu
        gauges_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Gauges', menu=gauges_menu)

        # Define the bars menu
        bars_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Bars', menu=bars_menu)

        # Populate the gauges menu
        for data_type in self.data_config:
            gauges_menu.add_command(label=data_type, command=lambda x=data_type: self.select_gauge(x))

        # Populate the bars menu
        for data_type in self.data_config:
            bars_menu.add_command(label=data_type, command=lambda x=data_type: self.select_bar(x))

    def select_gauge(self, selection):
        self.bar_widget.pack_forget()  # Hide the bar widget
        self.gauge_widget.pack(fill=BOTH, expand=True)  # Show the gauge widget

        if self.gauge_widget.canvas is not None:
            self.gauge_widget.canvas.destroy()  # Remove the gauge widget canvas

        if selection in self.data_config:
            gauge_data = self.data_config[selection]

            if selection in self.styles_config["gauge_styles"]:
                gauge_style = self.styles_config["gauge_styles"][selection]
            else:
                gauge_style = self.styles_config["gauge_styles"]["default"]

            self.gauge_widget.draw_gauge(gauge_data, gauge_style)

    def select_bar(self, selection):
        self.gauge_widget.pack_forget()  # Hide the gauge widget
        self.bar_widget.pack(fill=BOTH, expand=True)  # Show the bar widget

        if self.bar_widget.canvas is not None:
            self.bar_widget.canvas.destroy()  # Remove the bar widget canvas

        if selection in self.data_config:
            bar_data = self.data_config[selection]

            if selection in self.styles_config["bar_styles"]:
                bar_style = self.styles_config["bar_styles"][selection]
            else:
                bar_style = self.styles_config["bar_styles"]["default"]

            self.bar_widget.draw_bar(bar_data, bar_style)

    def read_serial_data(self):
        try:
            self.serial_port = serial.Serial(self.serial_config["port"], self.serial_config["baud_rate"])
            header_byte = self.serial_config["header_byte"]
            parameters = self.serial_config["parameters"]

            while True:
                data = self.serial_port.read(1)
                if data == header_byte:
                    parameter_index = self.serial_port.read(1)[0]
                    if parameter_index < len(parameters):
                        parameter = parameters[parameter_index]
                        value = float(self.serial_port.readline())
                        if parameter == self.gauge_widget.get_type():
                            self.gauge_widget.update_gauge(value)
                        if parameter == self.bar_widget.get_type():
                            self.bar_widget.update_bar(value)

        except serial.SerialException:
            print("Failed to open the serial port.")

    def start_serial_thread(self):
        self.serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
        self.serial_thread.start()

    def stop_serial_thread(self):
        if self.serial_port is not None:
            self.serial_port.close()
        if self.serial_thread is not None:
            self.serial_thread.join()

    def run(self):
        # Load configurations
        self.load_data_config("data_config.json")
        self.load_styles_config("styles_config.json")
        self.load_serial_config("serial_config.json")
        self.create_menu()

        self.gauge_widget.pack_forget()  # Hide the gauge widget initially
        self.bar_widget.pack_forget()  # Hide the bar widget initially

        self.start_serial_thread()

        self.parent.mainloop()

        self.stop_serial_thread()


if __name__ == '__main__':
    root = Tk()
    root.geometry("600x500")
    root.title("Telemetry Display")

    app = Application(root)
    app.run()
