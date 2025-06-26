# =========================================
# Ficheiro: sensor_plot.py
# =========================================

import serial
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

PORTA_SERIAL = '/dev/ttyUSB0'  # ou 'COM3' no Windows
BAUDRATE = 9600

class SensorPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico de Sensor 3 Eixos (MPU6050)")
        self.ax_data, self.ay_data, self.az_data = [], [], []

        self.canvas = Canvas(plt.figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_title("Aceleração (X, Y, Z)")
        self.ax.set_ylim(-20000, 20000)
        self.line_x, = self.ax.plot([], [], label='Ax')
        self.line_y, = self.ax.plot([], [], label='Ay')
        self.line_z, = self.ax.plot([], [], label='Az')
        self.ax.legend()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_grafico)
        self.timer.start(100)

        try:
            self.serial = serial.Serial(PORTA_SERIAL, BAUDRATE)
            self.leitura = threading.Thread(target=self.ler_dados)
            self.leitura.daemon = True
            self.leitura.start()
        except Exception as e:
            print(f"Erro ao abrir porta serial: {e}")

    def ler_dados(self):
        while True:
            try:
                linha = self.serial.readline().decode('utf-8').strip()
                ax, ay, az, *_ = map(int, linha.split(','))
                self.ax_data.append(ax)
                self.ay_data.append(ay)
                self.az_data.append(az)

                if len(self.ax_data) > 100:
                    self.ax_data.pop(0)
                    self.ay_data.pop(0)
                    self.az_data.pop(0)
            except:
                continue

    def atualizar_grafico(self):
        self.line_x.set_data(range(len(self.ax_data)), self.ax_data)
        self.line_y.set_data(range(len(self.ay_data)), self.ay_data)
        self.line_z.set_data(range(len(self.az_data)), self.az_data)
        self.ax.set_xlim(0, 100)
        self.canvas.draw()
