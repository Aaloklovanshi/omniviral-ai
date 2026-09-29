import json
import time
import urllib.request
import urllib.error
import os

LEADS_PATH = "marketing/outreach_leads/google_maps_leads.json"
BRIDGE_URL = "http://localhost:3000/send"

def send_whatsapp(phone, message):
    # Clean phone number for WhatsApp chatId format: <number>@s.whatsapp.net
    digits = "".join(filter(str.isdigit, phone))
    if len(digits) == 10:
        chat_id = f"91{digits}@s.whatsapp.net"
    elif len(digits) == 12 and digits.startswith("91"):
        chat_id = f"{digits}@s.whatsapp.net"
    else:
        chat_id = f"{digits}@s.whatsapp.net"

    payload = {
        "chatId": chat_id,
        "message": message
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BRIDGE_URL, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            return True, res_body
    except Exception as e:
        return False, str(e)

def main():
    if not os.path.exists(LEADS_PATH):
        print("Leads file not found!")
        return

    with open(LEADS_PATH, "r", encoding="utf-8") as f:
        leads = json.load(f)

    print(f"Loaded {len(leads)} leads. Starting autonomous batch outreach...")
    
    success_count = 0
    fail_count = 0

    for idx, lead in enumerate(leads, 1):
        phone = lead.get("phone")
        name = lead.get("business_name")
        pitch = lead.get("whatsapp_pitch")
        
        print(f"[{idx}/{len(leads)}] Reaching out to {name} ({phone})...", end=" ")
        
        success, res = send_whatsapp(phone, pitch)
        if success:
            print("✅ Delivered!")
            lead["outreach_status"] = "Delivered (Autonomous Batch)"
            success_count += 1
        else:
            print(f"❌ Failed: {res}")
            lead["outreach_status"] = f"Failed: {res}"
            fail_count += 1
        
        # Save progress every 10 leads
        if idx % 10 == 0:
            with open(LEADS_PATH, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)
            print(f"--- Checkpoint saved: {success_count} successful, {fail_count} failed ---")
        
        # Rate limit to avoid spam trigger
        time.sleep(2.0)

    # Final save
    with open(LEADS_PATH, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Batch outreach completed! Total Success: {success_count}, Total Failed: {fail_count}")

if __name__ == "__main__":
    main()
