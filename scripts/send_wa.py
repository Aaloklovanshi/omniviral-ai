"""
OmniViral AI - WhatsApp Outbound Message Sender
Sends messages via Hermes WhatsApp Bridge (port 3000)
"""
import sys
import json
import urllib.request
import urllib.parse

WHATSAPP_BRIDGE_URLS = ["http://localhost:3001/send", "http://localhost:3000/send"]

def send_whatsapp_message(phone_number: str, message: str):
    """
    Send WhatsApp message directly via Hermes WhatsApp Bridge.
    """
    clean_num = phone_number.strip().replace('+', '').replace(' ', '').replace('-', '')
    if not clean_num.startswith('91') and len(clean_num) == 10:
        clean_num = '91' + clean_num
        
    chat_id = f"{clean_num}@s.whatsapp.net"
    
    print(f"📱 Sending WhatsApp message to: {chat_id}")
    print(f"💬 Message: {message}")
    
    payload = json.dumps({
        "chatId": chat_id,
        "message": message
    }).encode('utf-8')
    
    for bridge_url in WHATSAPP_BRIDGE_URLS:
        try:
            req = urllib.request.Request(
                bridge_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                if res_data.get("success"):
                    print(f"✅ WhatsApp message delivered successfully via {bridge_url} to {chat_id}! MessageID: {res_data.get('messageId')}")
                    return True
                else:
                    print(f"⚠️ WhatsApp bridge response from {bridge_url}: {res_data}")
        except Exception as e:
            continue

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "8878707615"
    text = sys.argv[2] if len(sys.argv) > 2 else "hi i am alok"
    send_whatsapp_message(target, text)
