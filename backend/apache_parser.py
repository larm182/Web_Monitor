
import re

LOG_PATH = "/var/log/apache2/access.log"

def get_recent_visits(limit=1000):
    visits = []
    pattern = r'^(\S+) - - \[(.*?)\] "(\S+) (.*?) (HTTP/\d\.\d)" (\d{3}) .*?"(.*?)"$'
    try:
        with open(LOG_PATH, 'r') as f:
            lines = f.readlines()[-limit:]
        for line in lines:
            match = re.match(pattern, line)
            if match:
                ip, timestamp, method, url, _, status, user_agent = match.groups()
                visits.append({
                    "ip": ip,
                    "timestamp": timestamp,
                    "method": method,
                    "url": url,
                    "status": status,
                    "user_agent": user_agent
                })
    except Exception as e:
        print(f"Error al leer el log: {e}")
    return visits

def get_unique_ips():
    logs = get_recent_visits()
    return set(log['ip'] for log in logs)
