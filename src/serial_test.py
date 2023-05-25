import serial
import time

# Serial port settings
port = "USB Serial Port (COM3)"  # Choose a COM port number that is available on your system
baud_rate = 9600

# Test data format
header_byte = b'\xAA'  # The header byte that prefaces the data
# Parameters are as follows: "Vehicle Speed", "Engine RPM", "Water Temperature", "Air Fuel Ratio", "Battery Voltage"
parameters = [b'50', b'1230', b'150', b'14.7', b'13.9']  # Example parameter bytes

# Open the serial port
serial_port = serial.Serial(port, baud_rate)

# Send test data
while True:
    for parameter_index, parameter in enumerate(parameters):
        # Send the header byte
        serial_port.write(header_byte)
        # Send the parameter index byte
        serial_port.write(parameter)
        # Send the test value
        value = float(parameter_index + 1)  # Example test value
        serial_port.write(str(value).encode())
        # Wait for a short time before sending the next data
        time.sleep(0.5)

# Close the serial port
serial_port.close()

