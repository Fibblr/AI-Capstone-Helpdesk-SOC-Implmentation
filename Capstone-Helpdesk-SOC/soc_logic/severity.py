def calculate_risk(alert, confidence): 
    score = 0 
    # Failed attempts (35%) 
    score += min(alert["failed_attempts"] * 3, 35) 
    # External IP (25%) 
    if alert["external_ip"]: 
        score += 25 
    # After hours (15%) 
    if alert["after_hours"]: 
        score += 15 
    # Privileged account (15%) 
    if alert["privileged_account"]: 
        score += 15 
        
    # AI confidence (10%) 
    score += (confidence/100) * 10 
    return min(score, 100) 

def map_severity(score): 
    if score >= 85: 
        return "Critical" 
    elif score >= 70: 
        return "High" 
    elif score >= 40: 
        return "Medium" 
    else: 
        return "Low" 
