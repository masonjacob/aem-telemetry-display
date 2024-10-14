import serial
import time

class SerialConnection:
    def __init__(self, config_file):
        self.config = config_file
        self.port = self.config["port"]
        self.baud_rate = self.config["baud_rate"]
        self.serial_port = None

    def connect(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baud_rate)
            print(f"Serial port {self.port} connected.")
        except serial.SerialException as e:
            print(f"Serial port error: {e}")

    def disconnect(self):
        if self.serial_port:
            self.serial_port.close()
            print(f"Serial port {self.port} disconnected.")
            self.serial_port = None

    def send_data(self, data):
        if self.serial_port:
            try:
                self.serial_port.write(data.encode())
                print(f"Data sent: {data}")
            except serial.SerialException as e:
                print(f"Serial port write error: {e}")
        else:
            print("Serial port not connected. Cannot send data.")

    def receive_data(self):
        if self.serial_port:
            try:
                data = self.serial_port.readline().decode().strip()
                print(f"Data received: {data}")
                return data
            except serial.SerialException as e:
                print(f"Serial port read error: {e}")
        else:
            print("Serial port not connected. Cannot receive data.")
        return None
    
# # Example usage:
# serial_connection = SerialConnection("COM10", 9600)
# serial_connection.connect()
# serial_connection.send_data("Hello, Arduino!")
# received_data = serial_connection.receive_data()
# serial_connection.disconnect()

# # Example usage:
# serial_connection = SerialConnection("serial_config.json")
# serial_connection.connect()
# serial_connection.send_data("Hello, Arduino!")
# received_data = serial_connection.receive_data()
# serial_connection.disconnect()

class SerialEmulator:
    def __init__(self, config_file):
        self.config = config_file
        self.port = self.config["port"]
        self.baud_rate = self.config["baud_rate"]
        self.is_open = False

    def connect(self):
        if not self.is_open:
            self.is_open = True
            print(f"Serial port {self.port} connected.")

    def disconnect(self):
        if self.is_open:
            self.is_open = False
            print(f"Serial port {self.port} disconnected.")

    def send_data(self, data):
        if self.is_open:
            print(f"Sending data: {data}")
            # Emulate delay for data transmission
            time.sleep(0.1)

    def receive_data(self):
        if self.is_open:
            data = "Received data"
            print(f"Received data: {data}")
            return data

# # Example usage:
# serial_emulator = SerialEmulator("serial_config.json")
# serial_emulator.connect()
# serial_emulator.send_data("Hello, Arduino!")
# received_data = serial_emulator.receive_data()
# serial_emulator.disconnect()


