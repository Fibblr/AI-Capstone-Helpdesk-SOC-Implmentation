import json
import time
import requests

WAZUH_FILE = "/var/ossec/logs/alerts/alerts.json"
WEBHOOK = "http://172.18.76.215:8081/webhook"

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    print("after")
    print("Listening for authentication alerts...\n")

    with open(WAZUH_FILE, "r") as f:
        for line in follow(f):
            try:
                alert = json.loads(line)

                # Filter by description
                desc = alert.get("rule", {}).get("description", "").lower()

                if "login" not in desc and "authentication" not in desc:
                    continue

                res = requests.post(WEBHOOK, json=alert)

                print(f"Sent AUTH alert {alert.get('id')} → {res.status_code}")

            except Exception as e:
                print(f"Error: {e}")

main()