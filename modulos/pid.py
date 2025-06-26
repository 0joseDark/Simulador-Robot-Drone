# =========================================
# Ficheiro: modulos/pid.py
# =========================================

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox
import matplotlib.pyplot as plt

class JanelaPID(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador PID")
        self.layout = QVBoxLayout()
        self.form = QFormLayout()

        self.inputs = {}
        campos = ["Kp", "Ki", "Kd", "Erro Inicial", "Setpoint"]

        for campo in campos:
            entrada = QLineEdit()
            self.form.addRow(QLabel(campo), entrada)
            self.inputs[campo] = entrada

        self.botao = QPushButton("Simular")
        self.botao.clicked.connect(self.simular_pid)

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.botao)
        self.setLayout(self.layout)

    def simular_pid(self):
        try:
            Kp = float(self.inputs["Kp"].text())
            Ki = float(self.inputs["Ki"].text())
            Kd = float(self.inputs["Kd"].text())
            erro_inicial = float(self.inputs["Erro Inicial"].text())
            setpoint = float(self.inputs["Setpoint"].text())

            dt = 1  # passo de tempo
            tempo_total = 50
            tempos = list(range(tempo_total))
            erros = []
            saidas = []
            integral = 0
            erro_anterior = erro_inicial
            saida = 0

            for t in tempos:
                erro = setpoint - saida
                integral += erro * dt
                derivada = (erro - erro_anterior) / dt
                saida = Kp * erro + Ki * integral + Kd * derivada
                erros.append(erro)
                saidas.append(saida)
                erro_anterior = erro

            plt.figure(figsize=(6, 4))
            plt.plot(tempos, saidas, label="Saída PID")
            plt.plot(tempos, [setpoint]*tempo_total, '--', label="Setpoint")
            plt.xlabel("Tempo")
            plt.ylabel("Saída")
            plt.title("Resposta do Controlador PID")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro na simulação: {str(e)}")
