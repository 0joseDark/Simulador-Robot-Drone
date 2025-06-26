# Estrutura de pastas:
# ├── main.py
# ├── modulos/
# │   ├── __init__.py
# │   ├── simulador_fisico.py
# │   └── pid.py
# ├── sensor_plot.py
# └── log.py

# =========================================
# Ficheiro: main.py
# =========================================

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction
from modulos.simulador_fisico import SimuladorFisica
from sensor_plot import SensorPlot
from modulos.pid import JanelaPID

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulações Robô & Drone")
        self.resize(500, 150)

        menu = self.menuBar()
        sim_menu = menu.addMenu("Simulação Física")
        sensores_menu = menu.addMenu("Sensores")

        opcoes = ["Força", "Torque", "Resistência", "Tempo RC", "Energia Cinética", "Eficiência"]
        for nome in opcoes:
            acao = QAction(nome, self)
            acao.triggered.connect(lambda checked, n=nome: self.abrir_simulador(n))
            sim_menu.addAction(acao)

        acao_pid = QAction("Controlador PID", self)
        acao_pid.triggered.connect(self.abrir_pid)
        sim_menu.addAction(acao_pid)

        acao_sensores = QAction("MPU6050 em tempo real", self)
        acao_sensores.triggered.connect(self.abrir_sensor)
        sensores_menu.addAction(acao_sensores)

        botao_sair = QPushButton("Sair")
        botao_sair.clicked.connect(self.close)
        self.setCentralWidget(botao_sair)

    def abrir_simulador(self, tipo):
        self.sim = SimuladorFisica(tipo)
        self.sim.resize(500, 400)
        self.sim.show()

    def abrir_sensor(self):
        self.sensor = SensorPlot()
        self.sensor.show()

    def abrir_pid(self):
        self.pid = JanelaPID()
        self.pid.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
