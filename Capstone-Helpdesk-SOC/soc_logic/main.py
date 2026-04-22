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
    print("Listening to Wazuh alerts...\n")

    with open(WAZUH_FILE, "r") as f:
        for line in follow(f):
            try:
                alert = json.loads(line)

                res = requests.post(WEBHOOK, json=alert)

                print(f"Sent alert {alert.get('id')} → {res.status_code}")

            except Exception as e:
                print(f"Error: {e}")

main()
















# import json 
# from normalization import normalize 
# from client import classify_auth_alert
# from severity import calculate_risk, map_severity

# def mainsoc():
#     try:    
#         with open("alert_simulation.json") as f: 
#             alerts = json.load(f) 
#     except Exception as e:
#         print(f"Alerts Failed to Load: {e}")   
#     for alert in alerts: 
#         normalized = normalize(alert)
#         ai_output = classify_auth_alert(normalized) 
        
#         parsed = json.loads(ai_output) 
        
#         classification = parsed["classification"] 
        
#         confidence = parsed["confidence"] 
        
#         risk_score = calculate_risk(normalized, confidence) 
#         severity = map_severity(risk_score)
        
#         alert_id = normalized["alert_id"]
#         review_required = "".strip()
        
#         if severity == "Critical" or confidence < 70:
#             review_required = "YES"
#         else:
#             review_required = "NO" 
    
#         print("\n--------------------------------------")
#         print(f"\tAlert: {alert_id}\n\n")
#         print(f"\tClassification: {classification}\n\n")
#         print(f"\tConfidence: {confidence}\n\n")
#         print(f"\tRisk Score: {risk_score}\n\n")
#         print(f"\tSeverity: {severity}\n\n")
#         print(f"\tManual Review: {review_required}")
#         print("--------------------------------------\n")


# def main():
#     user = int(input("\nPick to access SOC(1) or IT HelpDesk Logs(2)\t"))
#     if user == 1 and user != 2:
#         mainsoc()
#     elif user == 2 and user != 1:
#         mainIT()
#     else:
#         print("Invalid")
#     return

# main()
