import nmap
import json
from datetime import datetime
import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"


MODO_TESTE = True  # Altera para False para usar scanner real

HISTORY_FILE = "data/history.json"
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

if not os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def fazer_rastreio():
    if MODO_TESTE:
        # Simulação de dispositivos fictícios
        dispositivos = [
            {
                "ip": "192.168.1.10",
                "hostname": "Dispositivo-Teste-1",
                "portas": [
                    {"porta": 22, "estado": "open", "protocolo": "tcp"},
                    {"porta": 80, "estado": "open", "protocolo": "tcp"},
                ]
            },
            {
                "ip": "192.168.1.25",
                "hostname": "Dispositivo-Teste-2",
                "portas": [
                    {"porta": 443, "estado": "open", "protocolo": "tcp"}
                ]
            },
            {
                "ip": "192.168.1.55",
                "hostname": "Impressora-Teste",
                "portas": []
            }
        ]

        resultado = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dispositivos": dispositivos
        }
        guardar_historico(resultado)
        return resultado

    else:
        nm = nmap.PortScanner()
        rede = "192.168.1.0/24"
        nm.scan(hosts=rede, arguments='-T4 -Pn -p 1-1000')

        dispositivos = []
        for host in nm.all_hosts():
            info = {
                "ip": host,
                "hostname": nm[host].hostname(),
                "portas": []
            }
            if 'tcp' in nm[host]:
                for porta in nm[host]['tcp']:
                    estado = nm[host]['tcp'][porta]
                    info["portas"].append({
                        "porta": porta,
                        "estado": estado['state'],
                        "protocolo": "tcp"
                    })
            dispositivos.append(info)

        resultado = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dispositivos": dispositivos
        }

        guardar_historico(resultado)
        return resultado


def guardar_historico(dados):
    historico = carregar_historico()
    historico.append(dados)
    with open(HISTORY_FILE , "w") as f:
        json.dump(historico, f, indent=2)

def carregar_historico():
    if os.path.exists(HISTORY_FILE ):
        with open(HISTORY_FILE , "r") as f:
            return json.load(f)
    return []
