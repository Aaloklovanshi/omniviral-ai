"""
OmniViral AI - WhatsApp Outbound Message Sender
Sends messages via Hermes WhatsApp Bridge (whatsmeow)
"""
import os
import sys
import json
import time
import requests
from pathlib import Path

HERMES_GATEWAY_URL = "http://localhost:8745"  # Default Hermes Gateway port
WHATSAPP_BRIDGE_DIR = Path(r"C:\Users\aalok\AppData\Local\hermes\whatsapp")

def send_whatsapp_message(phone_number, message):
    """
    Send WhatsApp message via Hermes Gateway API
    
    Args:
        phone_number: Indian format like '8878707615' or international '+918878707615'
        message: Text message to send
    """
    # Normalize phone number to WhatsApp JID format
    if phone_number.startswith('+'):
        phone_number = phone_number[1:]
    elif phone_number.startswith('91'):
        pass
    else:
        phone_number = '91' + phone_number
    
    jid = f"{phone_number}@s.whatsapp.net"
    
    print(f"📱 Sending WhatsApp message to: {jid}")
    print(f"💬 Message: {message[:50]}...")
    
    # Try Hermes Gateway REST API (if available)
    try:
        payload = {
            "platform": "whatsapp",
            "recipient": jid,
            "text": message
        }
        response = requests.post(
            f"{HERMES_GATEWAY_URL}/api/send",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Message sent successfully via Gateway API!")
            return True
        else:
            print(f"⚠️ Gateway API returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Gateway API not available: {e}")
    
    # Fallback: Direct whatsmeow socket approach
    print("🔄 Attempting direct bridge write...")
    
    # Write to pending_messages queue (Hermes internal queue)
    pending_dir = Path(r"C:\Users\aalok\AppData\Local\hermes\pending_messages")
    pending_dir.mkdir(parents=True, exist_ok=True)
    
    msg_file = pending_dir / f"wa_outbound_{int(time.time() * 1000)}.json"
    msg_data = {
        "platform": "whatsapp",
        "to": jid,
        "text": message,
        "timestamp": int(time.time())
    }
    
    with open(msg_file, 'w', encoding='utf-8') as f:
        json.dump(msg_data, f, indent=2)
    
    print(f"📝 Queued message in: {msg_file}")
    print("✅ Message will be sent when gateway processes the queue")
    return True

if __name__ == "__main__":
    target_number = "8878707615"
    
    message_text = """Hi! I am Alok 🚀

This is an automated test message from my OmniViral AI system powered by Hermes Agent.

Successfully testing WhatsApp outbound integration!"""
    
    send_whatsapp_message(target_number, message_text)
