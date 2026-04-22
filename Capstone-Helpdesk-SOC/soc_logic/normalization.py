from datetime import datetime

def external_ip(ip):
    if not ip:
        return False
    return not ip.startswith("192.168.")

def is_afterwork(timestamp):
    try:
        hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").hour
    except:
        return False
    return hour < 8 or hour > 18 

def normalize(alert):
    data = alert.get("data", {})
    rule = alert.get("rule", {})

    return {
        "alert_id": alert.get("id", "unknown"),
        "username": data.get("srcuser") or data.get("user") or "unknown",
        "failed_attempts": int(rule.get("level", 1)),
        "external_ip": external_ip(data.get("srcip", "")),
        "after_hours": is_afterwork(alert.get("timestamp", "")),
        "asset_criticality": "high" if rule.get("level", 0) > 10 else "low",
        "privileged_account": "admin" in str(data.get("srcuser", "")).lower(),
        "event_source": rule.get("groups", ["wazuh"])[0]
    }