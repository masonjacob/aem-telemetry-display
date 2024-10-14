import json
import threading
import tkinter as tk
# from tkinter.ttk import *
import time

# Class imports
from widgets.layout import Layout
from connection.serial_connection import SerialConnection
from configuration.config import Config

class Application(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = Config()
        self.main_layout = Layout(self, self.config_manager, "default")
        self.main_layout.pack()
        self.serial_connection = None
        self.incoming_serial_data = None
        self.serial_thread = None
        self.gauge_thread = None
        self.bar_thread = None

    def create_menu(self):
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        # # Define the gauges menu
        # gauges_menu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(label='Gauges', menu=gauges_menu)

        # # Define the bars menu
        # bars_menu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(label='Bars', menu=bars_menu)

        # # Populate the gauges menu
        # for data_type in self.config_manager.get_config("data_config"):
        #     gauges_menu.add_command(label=data_type, command=lambda x=data_type: self.select_gauge(x))

        # # Populate the bars menu
        # for data_type in self.config_manager.get_config("data_config"):
        #     bars_menu.add_command(label=data_type, command=lambda x=data_type: self.select_bar(x))

        # Define the layouts menu
        layouts_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Layouts', menu=layouts_menu)
        # Populate the layouts menu
        for layout in self.config_manager.get_config("layout_config"):
            layouts_menu.add_command(label=layout, command=lambda x=layout: self.select_layout(x))


        # Define the serial menu
        serial_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Serial', menu=serial_menu)
        serial_menu.add_command(label='Connect', command=self.connect_serial)
        serial_menu.add_command(label='Disconnect', command=self.disconnect_serial)
        serial_menu.entryconfig('Disconnect', state=tk.DISABLED)  # Initially disable Disconnect

    # def select_gauge(self, selection):
    #     data_config = self.config_manager.get_config("data_config")
    #     styles_config = self.config_manager.get_config("styles_config")

    #     self.bar_widget.pack_forget()  # Hide the bar widget
    #     self.gauge_widget.pack(fill=tk.BOTH, expand=True)  # Show the gauge widget

    #     if self.gauge_widget.canvas is not None:
    #         self.gauge_widget.canvas.destroy()  # Remove the gauge widget canvas

    #     if selection in data_config:
    #         gauge_data = data_config[selection]

    #         if selection in styles_config["gauge_styles"]:
    #             gauge_style = styles_config["gauge_styles"][selection]
    #         else:
    #             gauge_style = styles_config["gauge_styles"]["default"]

    #         self.gauge_widget.draw(gauge_data, gauge_style)

    #         self.update_idletasks()  # Update the window and its widgets

    #         if self.gauge_thread is None:
    #             self.gauge_thread = threading.Thread(target=self.update_gauge, daemon=True)
    #             self.gauge_thread.start()

    # def select_bar(self, selection):
    #     data_config = self.config_manager.get_config("data_config")
    #     styles_config = self.config_manager.get_config("styles_config")

    #     self.gauge_widget.pack_forget()  # Hide the gauge widget
    #     self.bar_widget.pack(fill=tk.BOTH, expand=True)  # Show the bar widget

    #     if self.bar_widget.canvas is not None:
    #         self.bar_widget.canvas.destroy()  # Remove the bar widget canvas

    #     if selection in data_config:
    #         bar_data = data_config[selection]

    #         if selection in styles_config["bar_styles"]:
    #             bar_style = styles_config["bar_styles"][selection]
    #         else:
    #             bar_style = styles_config["bar_styles"]["default"]

    #         self.bar_widget.draw(bar_data, bar_style)

    #         self.update_idletasks()  # Update the window and its widgets

    #         if self.bar_thread is None:
    #             self.bar_thread = threading.Thread(target=self.update_bar, daemon=True)
    #             self.bar_thread.start()

    def select_layout(self, selection):
        # if self.main_layout is not None:
        #     print(self.main_layout.layout_config)
        #     self.main_layout.erase()
        self.main_layout.set_layout(selection)
        self.update_idletasks()  # Update the window and its widgets


        # if self.gauge_thread is None:
        #     self.gauge_thread = threading.Thread(target=self.update_gauge, daemon=True)
        #     self.gauge_thread.start()

    def connect_serial(self):
        if self.serial_connection is None:
            self.serial_connection = SerialConnection(self.serial_config)
            self.serial_connection.connect()

            self.serial_thread = threading.Thread(target=self.receive_serial_data, daemon=True)
            self.serial_thread.start()

            self.parent.menu.entryconfig('Connect', state=tk.DISABLED)
            self.parent.menu.entryconfig('Disconnect', state=tk.NORMAL)

    def disconnect_serial(self):
        if self.serial_connection is not None:
            self.serial_connection.disconnect()
            self.serial_thread.join()
            self.serial_thread = None
            self.serial_connection = None

            self.parent.menu.entryconfig('Connect', state=tk.NORMAL)
            self.parent.menu.entryconfig('Disconnect', state=tk.DISABLED)

    def receive_serial_data(self):
        while True:
            if self.serial_connection is not None:
                data = self.serial_connection.receive_data()
                if data is not None:
                    self.incoming_serial_data = data

    # def update_gauge(self):
    #     gauge_type = self.gauge_widget.get_type()
    #     while True:
    #         if self.incoming_serial_data is not None:
    #             value = self.parse_serial_data(self.incoming_serial_data, gauge_type)
    #             self.gauge_widget.update(value)
    #             time.sleep(0.1)

    # def update_bar(self):
    #     bar_type = self.bar_widget.get_type()
    #     while True:
    #         if self.incoming_serial_data is not None:
    #             value = self.parse_serial_data(self.incoming_serial_data, bar_type)
    #             self.bar_widget.update(value)
    #             time.sleep(0.1)

    def parse_serial_data(self, data, parameter):
        # Parse the serial data and extract the value corresponding to the specified parameter
        # Modify this method according to the format of your incoming serial data
        # For example, if the format is "parameter:value", you can use:
        # tokens = data.split(':')
        # if len(tokens) == 2 and tokens[0] == parameter:
        #     return float(tokens[1])
        # else:
        #     return 0.0

        return 0.0

    def run(self):
        self.create_menu()
        self.pack()
        self.parent.mainloop()

        if self.serial_connection is not None:
            self.serial_connection.disconnect()

        if self.serial_thread is not None:
            self.serial_thread.join()

        if self.gauge_thread is not None:
            self.gauge_thread.join()

        if self.bar_thread is not None:
            self.bar_thread.join()

if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry("600x500")
    root.state("zoomed")
    root.title("Telemetry Display")
    app = Application(root)
    app.run()
