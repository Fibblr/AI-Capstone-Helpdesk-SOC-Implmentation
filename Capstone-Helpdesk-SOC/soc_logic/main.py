import json 
from normalization import normalize 
from client import classify_auth_alert
from severity import calculate_risk, map_severity

def mainsoc():
    try:    
        with open("alert_simulation.json") as f: 
            alerts = json.load(f) 
    except Exception as e:
        print(f"Alerts Failed to Load: {e}")   
    for alert in alerts: 
        normalized = normalize(alert)
        ai_output = classify_auth_alert(normalized) 
        
        parsed = json.loads(ai_output) 
        
        classification = parsed["classification"] 
        
        confidence = parsed["confidence"] 
        
        risk_score = calculate_risk(normalized, confidence) 
        severity = map_severity(risk_score)
        
        alert_id = normalized["alert_id"]
        review_required = "".strip()
        
        if severity == "Critical" or confidence < 70:
            review_required = "YES"
        else:
            review_required = "NO" 
    
        print("\n--------------------------------------")
        print(f"\tAlert: {alert_id}\n\n")
        print(f"\tClassification: {classification}\n\n")
        print(f"\tConfidence: {confidence}\n\n")
        print(f"\tRisk Score: {risk_score}\n\n")
        print(f"\tSeverity: {severity}\n\n")
        print(f"\tManual Review: {review_required}")
        print("--------------------------------------\n")


def main():
    user = int(input("\nPick to access SOC(1) or IT HelpDesk Logs(2)\t"))
    if user == 1 and user != 2:
        mainsoc()
    elif user == 2 and user != 1:
        mainIT()
    else:
        print("Invalid")
    return

main()
