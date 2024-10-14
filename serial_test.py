import serial

# Define serial port settings
port = 'COM3'  # Replace with the appropriate port name on your system
baudrate = 19200
# timeout = 1  # Timeout for read operations (in seconds)
header_byte = b'\x55'  # Replace with the actual header byte
data_bits = serial.EIGHTBITS  # Number of data bits (7, 8)
stop_bits = serial.STOPBITS_ONE  # Number of stop bits (1, 1.5, 2)

# Create a serial object
ser = serial.Serial(port, baudrate, bytesize=data_bits, stopbits=stop_bits)

# Check if the serial port is open
if ser.is_open:
    print(f"Serial port {port} is open.")

    # Read incoming data
    while True:
        try:
            # Read a byte of data from the serial port
            received_byte = ser.read(21)
            print(received_byte)

            # # Check if the received byte matches the header byte
            # if received_byte == header_byte:
            #     # Read the remaining data
            #     data = ser.readline().decode().strip()

            #     # Process the received data
            #     print(f"Received data: {data}")

        except KeyboardInterrupt:
            # Break the loop on keyboard interrupt
            break

    # Close the serial port
    ser.close()
    print(f"Serial port {port} is closed.")

else:
    print(f"Failed to open serial port {port}.")

#################################################
# Notes
#################################################
# Example of recieved data
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x001\x02\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xe9U\x002\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xebU\x002\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xebU\x001\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x001\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x001\x03\x18\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xe9U\x001\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x002\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xebU\x002\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xebU\x002\x02\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x001\x03\x19\x17\xff'
# b'\xff\x01\xff\xff\xff\xff\x94\xb9\xbe\x00\x00\x00\x80\xeaU\x002\x03\x19\x17\xff'

# Thoughts:
# I believe that the data is inverted, and in order to get the actual value 
# I need to apply the scalar, then the offset, and then compare it to min and max value

# Possible Decode Fuction