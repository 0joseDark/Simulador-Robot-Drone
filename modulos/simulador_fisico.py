# =========================================
# Ficheiro: modulos/simulador_fisico.py
# =========================================

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from log import gravar_log, ler_logs

class SimuladorFisica(QWidget):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.setWindowTitle(f"Simulador: {tipo}")
        self.layout = QVBoxLayout()
        self.form = QFormLayout()
        self.inputs = {}

        self.campos = {
            "Força": ["Massa (kg)", "Aceleração (m/s²)"],
            "Torque": ["Força (N)", "Raio (m)"],
            "Resistência": ["Resistividade (ρ)", "Comprimento (m)", "Área (m²)"],
            "Tempo RC": ["Resistência (Ω)", "Capacitância (F)"],
            "Energia Cinética": ["Massa (kg)", "Velocidade (m/s)"],
            "Eficiência": ["Saída (W)", "Entrada (W)"]
        }

        for campo in self.campos[tipo]:
            entrada = QLineEdit()
            self.form.addRow(QLabel(campo), entrada)
            self.inputs[campo] = entrada

        self.resultado = QLabel("Resultado: ")
        self.botao = QPushButton("Calcular")
        self.botao.clicked.connect(self.calcular)

        self.botaoGrafico = QPushButton("Mostrar Gráfico")
        self.botaoGrafico.clicked.connect(self.mostrar_grafico)

        self.resultadosAntigos = QTextEdit()
        self.resultadosAntigos.setReadOnly(True)
        self.carregar_resultados()

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.botao)
        self.layout.addWidget(self.botaoGrafico)
        self.layout.addWidget(self.resultado)
        self.layout.addWidget(QLabel("Últimos cálculos:"))
        self.layout.addWidget(self.resultadosAntigos)
        self.setLayout(self.layout)

    def calcular(self):
        try:
            if self.tipo == "Força":
                m = float(self.inputs["Massa (kg)"].text())
                a = float(self.inputs["Aceleração (m/s²)"].text())
                resultado = m * a
                formula = f"F = m*a = {m}*{a} = {resultado:.2f} N"

            elif self.tipo == "Torque":
                f = float(self.inputs["Força (N)"].text())
                r = float(self.inputs["Raio (m)"].text())
                resultado = f * r
                formula = f"τ = F*r = {f}*{r} = {resultado:.2f} N·m"

            elif self.tipo == "Resistência":
                ρ = float(self.inputs["Resistividade (ρ)"].text())
                l = float(self.inputs["Comprimento (m)"].text())
                A = float(self.inputs["Área (m²)"].text())
                resultado = ρ * l / A
                formula = f"R = ρ*l/A = {ρ}*{l}/{A} = {resultado:.6f} Ω"

            elif self.tipo == "Tempo RC":
                R = float(self.inputs["Resistência (Ω)"].text())
                C = float(self.inputs["Capacitância (F)"].text())
                resultado = R * C
                formula = f"t = R*C = {R}*{C} = {resultado:.3f} s"

            elif self.tipo == "Energia Cinética":
                m = float(self.inputs["Massa (kg)"].text())
                v = float(self.inputs["Velocidade (m/s)"].text())
                resultado = 0.5 * m * v**2
                formula = f"E = 0.5*m*v² = 0.5*{m}*{v}² = {resultado:.2f} J"

            elif self.tipo == "Eficiência":
                saida = float(self.inputs["Saída (W)"].text())
                entrada = float(self.inputs["Entrada (W)"].text())
                resultado = (saida / entrada) * 100
                formula = f"η = (Saída/Entrada)*100 = ({saida}/{entrada})*100 = {resultado:.2f}%"

            self.resultado.setText("Resultado: " + formula)
            gravar_log(self.tipo, formula)
            self.carregar_resultados()

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro no cálculo: {str(e)}")

    def mostrar_grafico(self):
        try:
            x_vals, y_vals = [], []
            titulo, xlabel, ylabel = "", "", ""

            if self.tipo == "Força":
                a = float(self.inputs["Aceleração (m/s²)"].text())
                x_vals = list(range(1, 11))
                y_vals = [m * a for m in x_vals]
                titulo = "Força vs Massa"
                xlabel, ylabel = "Massa (kg)", "Força (N)"

            elif self.tipo == "Torque":
                f = float(self.inputs["Força (N)"].text())
                x_vals = [i / 10 for i in range(1, 21)]
                y_vals = [f * r for r in x_vals]
                titulo = "Torque vs Raio"
                xlabel, ylabel = "Raio (m)", "Torque (N·m)"

            elif self.tipo == "Resistência":
                ρ = float(self.inputs["Resistividade (ρ)"].text())
                l = float(self.inputs["Comprimento (m)"].text())
                x_vals = [i / 10 for i in range(1, 21)]
                y_vals = [ρ * l / A for A in x_vals]
                titulo = "Resistência vs Área"
                xlabel, ylabel = "Área (m²)", "Resistência (Ω)"

            elif self.tipo == "Tempo RC":
                R = float(self.inputs["Resistência (Ω)"].text())
                x_vals = [i / 1000 for i in range(1, 1001, 50)]
                y_vals = [R * C for C in x_vals]
                titulo = "Tempo vs Capacitância"
                xlabel, ylabel = "Capacitância (F)", "Tempo (s)"

            plt.figure(figsize=(5, 4))
            plt.plot(x_vals, y_vals, marker="o")
            plt.title(titulo)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            QMessageBox.warning(self, "Erro no gráfico", str(e))

    def carregar_resultados(self):
        ultimos = ler_logs(self.tipo, 10)
        self.resultadosAntigos.setText("\n".join(ultimos))

