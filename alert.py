import time
from collections import defaultdict
import requests
from datetime import datetime, timedelta

# Configura esto
LOG_PATH = "/var/log/apache2/access.log"
TOKEN = "Tu_Token"
CHAT_ID = "ID"
THRESHOLD = 30  # peticiones
WINDOW_SECONDS = 60  # en segundos

def send_telegram_alert(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def parse_apache_log_line(line):
  
    try:
        ip = line.split(" ")[0]
        time_str = line.split("[")[1].split("]")[0].split()[0]
        timestamp = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S")
        return ip, timestamp
    except Exception:
        return None, None

def monitor_log():
    ip_hits = defaultdict(list)

    while True:
        now = datetime.now()
        with open(LOG_PATH, "r") as log_file:
            for line in log_file:
                ip, timestamp = parse_apache_log_line(line)
                if not ip or not timestamp:
                    continue
                if (now - timestamp).total_seconds() <= WINDOW_SECONDS:
                    ip_hits[ip].append(timestamp)

        for ip, timestamps in ip_hits.items():
            if len(timestamps) > THRESHOLD:
                print(f"[!] Alerta: {ip} hizo {len(timestamps)} peticiones en {WINDOW_SECONDS} segundos.")
                send_telegram_alert(TOKEN, CHAT_ID, f"🚨 IP sospechosa: {ip} hizo {len(timestamps)} peticiones en {WINDOW_SECONDS} segundos.")
        
        ip_hits.clear()
        time.sleep(10)  

if __name__ == "__main__":
    monitor_log()
