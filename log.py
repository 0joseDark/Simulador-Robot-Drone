# =========================================
# Ficheiro: log.py
# =========================================

import os
from datetime import datetime

LOG_FILE = "simulacoes.log"

def gravar_log(tipo, linha):
    """Grava uma linha de resultado no ficheiro de log com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {tipo}: {linha}\n")

def ler_logs(tipo, ultimos_n=10):
    """Lê os últimos 'n' resultados do tipo indicado."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        linhas = f.readlines()
    filtradas = [linha.strip() for linha in linhas if tipo in linha]
    return filtradas[-ultimos_n:]
