import serial
import threading
import os

# Create a global variable to signal to the threads when to stop
stop = False

#choose the serial connection based on the OS
def choose_serial():
    #if the running OS is windows use the windows serial connection
    if os.name == 'nt':
        #find the COM port of the serial connection and return it
        for i in range(256):
            try:
                #try to open the COM port as string
                s = serial.Serial("COM" + str(i), 115200)
                s.close()
                #output the COM port number and make the background of the print green
                print("\033[92m" + "COM port found! COM port: " + str(i) + "\033[0m")
                return serial.Serial("COM" + str(i), 115200)
            except serial.SerialException:
                pass
        #if no COM port is found, return an error and make the background of the print red
        print("\033[91m" + "ERROR: No COM port found!" + "\033[0m")

    #if the running OS is linux use the linux serial connection
    elif os.name == 'posix':
        return serial.Serial('/dev/ttyUSB0', 115200)

# Define a function for reading from the serial connection
def read_from_serial():
    #set the serial connection type based on the OS
    ser = choose_serial()

    global stop
    while not stop:
        # Read data from the serial connection
        data = ser.readline()

        # Print the data to the terminal
        print(data)

        # Check if the command "success" has been received
        if data == b'success\n':
            # Signal to the threads to stop
            stop = True

# Define a function for writing to the serial connection
def write_to_serial(send_data):
    #set the serial connection type based on the OS
    ser = choose_serial()

    global stop
    while not stop:
        #send the send_data to the drone
        ser.write(send_data.encode())
        #after sending the data, send the string "complete" to the drone
        ser.write("complete".encode())

# Define a function for closing the serial connection
def close_serial():
    #set the serial connection type based on the OS
    ser = choose_serial()

    # Close the serial connection
    ser.close()

# Create a thread for reading from the serial connection
read_thread = threading.Thread(target=read_from_serial)
# Create a thread for writing to the serial connection
write_thread = threading.Thread(target=write_to_serial)

