
import subprocess

def block_ip(ip):
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

def unblock_ip(ip):
    subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])

def get_blocked_ips():
    output = subprocess.check_output(["sudo", "iptables", "-L", "INPUT", "-n"]).decode()
    return [line.split()[3] for line in output.splitlines() if "DROP" in line]
