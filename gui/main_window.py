from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QLabel, QPushButton, QLineEdit, QTextEdit
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
import pyqtgraph as pg
from serial_connection import SerialConnection


class MainWindow(QMainWindow):
    promotie: str = "2024-2025"
    team: list[str] = [
        "Popa Irina-Gabriela",
        "Sandu Dragos-Nicolae",
    ]
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Proiect Microprocesoare {self.promotie}")
        self.setWindowIcon(QIcon("./icon.png"))
        

        primary_layout = QVBoxLayout()
        secondary_layout = QHBoxLayout()
        tertiary_layout = QVBoxLayout()

        team_box = QGroupBox("Membrii echipei")
        bold_font = QFont()
        bold_font.setBold(True)
        team_box.setFont(bold_font)

        first_member = QLabel(f"Membru 1: {self.team[0]}")
        second_member = QLabel(f"Membru 2: {self.team[1]}")
        team_box_layout = QVBoxLayout()
        team_box_layout.addWidget(first_member,1)
        team_box_layout.addWidget(second_member,1)
        team_box.setLayout(team_box_layout)

        control_panel_box = QGroupBox("Control Panel")
        control_panel_box.setFont(bold_font)

        button1 = QPushButton("Toggle LED Direction")
        button1.clicked.connect(self.toggle_led_direction)

        control_panel_box_layout = QVBoxLayout()
        control_panel_box_layout.setSpacing(5)
        control_panel_box_layout.addWidget(button1,1)

        control_panel_box_layout.addStretch()

        control_panel_box.setLayout(control_panel_box_layout)

        tertiary_layout.addWidget(team_box, 1)
        tertiary_layout.addWidget(control_panel_box,5)

        #Initialize SerialConnection
        self.serial = SerialConnection("COM4")
        self.serial.data_received.connect(self.update_plot_and_debug)


         # Plot Widget
        self.plot_widget = pg.PlotWidget()
        #self.plot_widget.setBackground("b")
        self.plot_widget.setTitle("Voltage vs Time")
        self.plot_widget.setLabel("left", "Voltage (V)")
        self.plot_widget.setLabel("bottom", "Time (s)")
        self.plot_data = self.plot_widget.plot([], [], pen="b")  # Dynamic plot

        self.time_data = []  # Time axis
        self.voltage_data = []  # Voltage values
        self.time_counter = 0  # Keep track of time


        secondary_layout.addWidget(self.plot_widget, 3)
        secondary_layout.addLayout(tertiary_layout, 1)

        primary_layout.addLayout(secondary_layout, 4)

        self.debug_box = QTextEdit()
        self.debug_box.setReadOnly(True)

        debug_box = QGroupBox("Debug")
        debug_box_layout = QVBoxLayout()
        debug_box_layout.addWidget(self.debug_box, 1)
        debug_box.setLayout(debug_box_layout)

        primary_layout.addWidget(debug_box, 2)

        widget = QWidget()
        widget.setLayout(primary_layout)
        
        self.setCentralWidget(widget)


    def update_plot_and_debug(self, data: str):
        """Update the plot and debug box with the new voltage reading."""
        # Update debug box
        voltage = float(data)
        self.debug_box.append(f"Received Voltage: {voltage:.1f} V")

        # Update time and voltage data
        self.time_data.append(self.time_counter)
        self.voltage_data.append(voltage)
        self.time_counter += 1

        # Determine the pen color based on the voltage value
        if voltage < 2.0:
            pen = pg.mkPen(color="green", width=5)
        elif voltage < 4.0:
            pen = pg.mkPen(color="yellow", width=5)
        else:
            pen = pg.mkPen(color="red", width=5)

        # Create a new plot item for each segment
        if len(self.time_data) > 1:
            self.plot_widget.plot(
                self.time_data[-2:],  # Last two time points
                self.voltage_data[-2:],  # Last two voltage points
                pen=pen,
                clear=False,  # Do not clear the previous data
            )

    
    def toggle_led_direction(self):
        """Send a command to toggle the LED direction."""
        self.serial.write_data('c')



    def closeEvent(self, event):
        """Clean up on application exit."""
        self.serial.close_connection()
        super().closeEvent(event)