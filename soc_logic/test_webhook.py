import requests
import json

# Your Flask app's webhook URL (Notice we are using port 8081 to match your app.py)
url = "http://127.0.0.1:8081/webhook"

# One of Cameron's simulated alerts
payload = {
    "alert_id": "AUTH-1002",
    "timestamp": "2026-02-15 10:15:00",
    "username": "asmith",
    "source_ip": "192.168.1.44",
    "failed_attempts": 2,
    "event_source": "VPN",
    "asset_criticality": "Low",
    "privileged_account": False
}

print(f"Sending alert {payload['alert_id']} to {url}...\n")

try:
    # Shoot the JSON payload to your Flask app
    response = requests.post(url, json=payload)

    # Print the results!
    print(f"Status Code: {response.status_code}")
    print("Response from your Helpdesk App:")
    print(json.dumps(response.json(), indent=4))

except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect. Make sure your Flask app.py is running in another tab!")