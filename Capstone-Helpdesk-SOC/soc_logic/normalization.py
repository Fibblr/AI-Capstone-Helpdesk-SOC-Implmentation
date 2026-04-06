from datetime import datetime

def external_ip(ip):
    return not ip.startswith("192.168.")
def is_afterwork(timestamp):
    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
    return hour < 8 or hour > 18 
def normalize(alert): 
    return {
        "alert_id": alert.get("alert_id"), 
        "username": alert.get("username"), 
        "failed_attempts": alert.get("failed_attempts", 0), 
        "external_ip": external_ip(alert.get("source_ip", "0.0.0.0")), 
        "after_hours": is_afterwork(alert.get("timestamp", "1970-01-01 00:00:00")), 
        "asset_criticality": alert.get("asset_criticality", "low"), 
        "privileged_account": alert.get("privileged_account", False), 
        "event_source": alert.get("event_source", "unknown")
    } 
