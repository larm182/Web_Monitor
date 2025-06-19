
from flask import Flask, jsonify, request, render_template
from apache_parser import get_recent_visits, get_unique_ips
from metrics import get_system_metrics, get_top_processes
from firewall import block_ip, get_blocked_ips, unblock_ip
from telegram_alert import send_telegram_alert
import json
import threading
import time
from datetime import datetime
from collections import defaultdict

THRESHOLD = 10  # Máximo permitido en intervalo
WINDOW_SECONDS = 60  # Intervalo de análisis (segundos)
alerted_ips = set()  # Para evitar spam de alertas repetidas

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Cargar configuración Telegram
with open("../config.json") as f:
    CONFIG = json.load(f)

token = CONFIG.get("telegram_token")
chat_id = CONFIG.get("telegram_chat_id")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/traffic")
def traffic():
    logs = get_recent_visits()
    return jsonify(logs)

@app.route("/api/ips")
def unique_ips():
    ips = get_unique_ips()
    return jsonify({"total": len(ips), "ips": list(ips)})

@app.route("/api/metrics")
def metrics():
    data = get_system_metrics()
    data["top_processes"] = get_top_processes()
    return jsonify(data)

@app.route("/api/block", methods=["POST"])
def block():
    ip = request.json.get("ip")
    reason = request.json.get("reason", "Manual")
    if ip:
        block_ip(ip)
        send_telegram_alert(token, chat_id, f"IP bloqueada: {ip}\nMotivo: {reason}")
        return jsonify({"status": "success", "ip": ip})
    return jsonify({"status": "error"}), 400

@app.route("/api/blocked")
def blocked():
    return jsonify(get_blocked_ips())

@app.route("/api/unblock", methods=["POST"])
def unblock():
    ip = request.json.get("ip")
    if ip:
        unblock_ip(ip)
        return jsonify({"status": "unblocked", "ip": ip})
    return jsonify({"status": "error"}), 400

@app.route("/api/telegram", methods=["POST"])
def send_alert():
    data = request.json
    msg = f"🔔 Alerta ({data.get('type', 'Manual')})\nSeveridad: {data.get('severity')}\nMensaje: {data.get('message')}"
    send_telegram_alert(token, chat_id, msg)
    return jsonify({"status": "sent"})

def monitor_traffic():
    while True:
        try:
            visits = get_recent_visits()  # [{'ip': '1.2.3.4', 'timestamp': '11/Jun/2025:12:00:01'}, ...]
            now = datetime.now()
            ip_hits = defaultdict(list)

            for entry in visits:
                ip = entry["ip"]
                raw_timestamp = entry["timestamp"]

                # Intenta parsear el string de timestamp
                try:
                    timestamp = datetime.strptime(raw_timestamp, "%d/%b/%Y:%H:%M:%S")
                except ValueError:
                    try:
                        timestamp = datetime.fromisoformat(raw_timestamp)
                    except ValueError:
                        continue  # Si no se puede parsear, ignora esta línea

                # Ahora sí se puede comparar
                if (now - timestamp).total_seconds() <= WINDOW_SECONDS:
                    ip_hits[ip].append(timestamp)

            for ip, timestamps in ip_hits.items():
                if len(timestamps) > THRESHOLD and ip not in alerted_ips:
                    msg = f"🚨 IP sospechosa: {ip} hizo {len(timestamps)} peticiones en {WINDOW_SECONDS} segundos."
                    send_telegram_alert(token, chat_id, msg)
                    print(f"[!] Alerta: {ip} hizo {len(timestamps)} peticiones en {WINDOW_SECONDS} segundos.")
                    block_ip(ip)
                    alerted_ips.add(ip)

        except Exception as e:
            print(f"[monitor_traffic] Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    thread = threading.Thread(target=monitor_traffic, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=8080, debug=True)
