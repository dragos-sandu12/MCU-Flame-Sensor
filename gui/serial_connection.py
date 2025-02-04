import re
from PySide6.QtCore import QObject, Signal, QThread
import serial

class SerialConnection(QObject):
    data_received = Signal(str)  # Signal to emit received data

    def __init__(self, port, baud_rate=14400, timeout=1):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)

        # Start the thread for reading data
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.read_data)
        self.thread.start()

    def read_data(self):
        """Continuously read data from the serial port."""
        while True:
            if self.serial.is_open:
                try:
                    data = self.serial.readline().decode().strip()  # Read and decode a line
                    if data:
                        # Use regex to extract numeric values from the string
                        match = re.search(r"Value\s*=\s*([\d.]+)", data)
                        if match:
                            value = match.group(1)  # Extract the numeric value
                            self.data_received.emit(value)  # Emit the numeric part
                        else:
                            self.data_received.emit("Error: Invalid data format")
                except serial.SerialException as e:
                    self.data_received.emit(f"Error: {str(e)}")


    def write_data(self, data: str):
        """Send data to the serial port."""
        if self.serial.is_open:
            try:
                self.serial.write(data.encode())  # Write the string as bytes
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")


    def close_connection(self):
        """Close the serial port and thread."""
        if self.serial.is_open:
            self.serial.close()
        self.thread.quit()
        self.thread.wait()
