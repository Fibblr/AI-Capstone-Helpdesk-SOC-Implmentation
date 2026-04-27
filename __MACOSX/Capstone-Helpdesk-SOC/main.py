import json
import time
import requests

WAZUH_FILE = "/var/ossec/logs/alerts/alerts.json"
WEBHOOK = "http://192.168.1.51:8081/webhook"  

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def safe_parse(line):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None

def main():
    print("Listening for authentication alerts...\n")

    with open(WAZUH_FILE, "r") as f:
        for line in follow(f):

            alert = safe_parse(line)
            if not alert:
                continue

            rule = alert.get("rule", {})
            desc = rule.get("description", "").lower()
            groups = [g.lower() for g in rule.get("groups", [])]

            is_auth = (
                "authentication" in desc or
                "login" in desc or
                "sshd" in groups or
                "authentication_failed" in groups
            )

            if not is_auth:
                continue

            try:
                res = requests.post(WEBHOOK, json=alert)
                print(f"Sent AUTH alert {alert.get('id')} → {res.status_code}")
            except Exception as e:
                print(f"Webhook error: {e}")

main()