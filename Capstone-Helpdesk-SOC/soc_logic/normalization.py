from datetime import datetime

def external_ip(ip):
    return not ip.startswith("192.168.")
def is_afterwork(timestamp):
    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
    return hour < 8 or hour > 18 
def normalize(alert):
    data = alert.get("data", {})

    # Username fallback
    username = (
        data.get("user") or
        data.get("srcuser") or
        data.get("dstuser") or
        "unknown"
    )

    # Safe attempts parsing
    try:
        attempts = int(data.get("attempts", 0))
    except:
        attempts = 0

    # Boolean fix
    privileged = str(data.get("privileged_account", "false")).lower() == "true"

    return {
        "alert_id": alert.get("id", "unknown"),
        "username": username,
        "failed_attempts": attempts,
        "external_ip": external_ip(data.get("srcip", "0.0.0.0")),
        "after_hours": is_afterwork(alert.get("timestamp", "1970-01-01 00:00:00")),
        "asset_criticality": "high" if data.get("asset_criticality", "low").lower() == "high" else "low",
        "privileged_account": privileged,
        "event_source": alert.get("rule", {}).get("groups", ["unknown"])[0]
    }