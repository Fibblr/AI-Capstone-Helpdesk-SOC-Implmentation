import cohere
import logging 
from config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)

logging.basicConfig(filename='cohere.log', level=logging.ERROR)

def raisederror(e):
    logging.error(f"AI Failed to Parse: {str(e)}")
    print("Failure Logged to 'cohere.log'")
    

def classify_auth_alert(alert):
    try:
        prompt_text = f"""
        You are a SOC authentication alert classifier.

        Return ONLY raw JSON.
        Do NOT include explanation.
        Do NOT include markdown.
        Do NOT include backticks.

        Format exactly like this:
        {{
        "classification": "",
        "confidence": 0
        }}

        Alert:
        {alert}
        """
        response = co.chat(
            model="command-a-03-2025",
            message=prompt_text,
            max_tokens=150,
            temperature=0
        )
    except Exception as e:
        ("Failed to recieve AI Feedback, Sending to manual review")
        raisederror(e)
        
    return '{"classification": "Unknown", "confidence": 0}'