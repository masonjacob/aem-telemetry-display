from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import json

class TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Telemetry Display")
        self.root.geometry("800x600")

        self.layouts = []
        self.load_layouts()

        self.home_tab = self.create_home_tab()
        self.editor_tab = self.create_editor_tab()

        self.tab_control = Notebook(self.root)
        self.tab_control.add(self.home_tab, text="Home")
        self.tab_control.add(self.editor_tab, text="Editor")
        self.tab_control.pack(expand=True, fill=BOTH)

    def load_layouts(self):
        try:
            with open("layouts.json") as file:
                data = json.load(file)
                self.layouts = data
        except FileNotFoundError:
            messagebox.showerror("Error", "Layouts file not found.")

    def create_home_tab(self):
        home_frame = Frame(self.root)
        home_frame.pack(pady=20)

        label = Label(home_frame, text="Select Layout:")
        label.grid(row=0, column=0)

        self.layout_var = StringVar()
        layout_names = [layout['name'] for layout in self.layouts]
        layout_dropdown = OptionMenu(home_frame, self.layout_var, *layout_names)
        layout_dropdown.grid(row=0, column=1)

    def create_editor_tab(self):
        editor_frame = Frame(self.root)
        editor_frame.pack(pady=20)

        label = Label(editor_frame, text="Select Editor:")
        label.grid(row=0, column=0)

        self.editor_var = StringVar()
        editor_dropdown = OptionMenu(editor_frame, self.editor_var, "Gauges", "Bars")
        editor_dropdown.grid(row=0, column=1)

        self.editor_canvas = Canvas(editor_frame, width=400, height=300, bg="white")
        self.editor_canvas.grid(row=1, columnspan=2, padx=10, pady=10)

        self.create_editor()

    def create_editor(self):
        self.editor_canvas.delete("all")
        editor_choice = self.editor_var.get()

        if editor_choice == "Gauges":
            self.create_gauges_editor(self.editor_canvas)
        elif editor_choice == "Bars":
            self.create_bars_editor(self.editor_canvas)

    def create_gauges_editor(self, frame):
        pass
        # Add gauge editor logic here

    def create_bars_editor(self, frame):
        pass
        # Add bar editor logic here

root = Tk()
app = TelemetryApp(root)
root.mainloop()
