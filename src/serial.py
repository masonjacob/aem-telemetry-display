import time
from enum import Enum

# Parity options
class Parity(Enum):
    NONE = 0
    EVEN = 1
    ODD = 2

# Emulate Serial Port
class SerialPortEmulator:
    def __init__(self, baudrate, parity):
        self.baudrate = baudrate
        self.parity = parity
        self.data = "42.5,10,80"  # Example data: value1,value2,value3

    def open(self):
        pass

    def close(self):
        pass

    def read(self, size):
        # Emulate reading data from a serial port
        data = self.data
        if self.parity != Parity.NONE:
            # Add parity bit
            parity_bit = self.calculate_parity_bit(data)
            data += parity_bit

        return data.encode()

    def calculate_parity_bit(self, data):
        # Calculate parity bit based on parity option
        if self.parity == Parity.EVEN:
            count = sum(int(bit) for bit in data) + 1
            return str(count % 2)
        elif self.parity == Parity.ODD:
            count = sum(int(bit) for bit in data)
            return str(count % 2)
        else:
            return ''


# Example usage
port = SerialPortEmulator(baudrate=9600, parity=Parity.ODD)
port.open()

while True:
    # Read data from the serial port
    data = port.read(1024)

    # Process the data
    values = data.decode().strip().split(',')
    value1, value2, value3 = map(float, values)
    # Process the values as needed...

    # Delay before reading again
    time.sleep(1)

port.close()
