import os
import sys
import time
import json
import re
import urllib.request
from datetime import datetime

INBOUND_LOG_PATH = r"C:/Users/aalok/AppData/Local/hermes/whatsapp/inbound_messages.jsonl"
OUTREACH_DB_PATH = r"C:/Users/aalok/omniviral-ai/marketing/outreach_leads/google_maps_leads.json"
BRIDGE_URL = "http://localhost:3000/send"
PROCESSED_FILE = r"C:/Users/aalok/omniviral-ai/marketing/outreach_leads/processed_msg_hashes.json"

DEMO_SALON = "https://aaloklovanshi.github.io/omniviral-ai/demo_salon.html"
DEMO_DENTAL = "https://dr-shrivastava-dental.lovable.app"
DEMO_INTERIOR = "https://aaloklovanshi.github.io/omniviral-ai/demo_interior.html"

def send_wa(target_jid, message):
    try:
        payload = json.dumps({"chatId": target_jid, "message": message}).encode("utf-8")
        req = urllib.request.Request(BRIDGE_URL, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode())
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto-Replied to {target_jid}: {data}")
            return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Send Error to {target_jid}: {e}")
        return False

def get_clean_phone(raw_str):
    m = re.findall(r"\b\d{10}\b", raw_str)
    return m[0] if m else None

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed(hashes):
    try:
        with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
            json.dump(list(hashes), f)
    except:
        pass

def generate_reply(text, sender_info):
    lower = text.lower()
    
    # Check if automated welcome message from business (e.g. Amyra Beauty Junction)
    if "thank you for contacting" in lower or "welcome to" in lower or "how we can help" in lower:
        if "amyra" in lower or "beauty" in lower or "salon" in lower:
            return f"""Namaste Ma'am/Sir 🙏

Mera naam Alok hai (Bhopal Digital Growth Studio).
Maine Piplani me aapka *Amyra Beauty Junction & Bridal Studio* dekha tha. Google par 4.8★ rating bohot hi outstanding hai! 👏

Bridal bookings aur salon appointments direct lene ke liye humne ek exclusive VIP Salon & Bridal Booking Web Portal ready kiya hai:
👉 *Live Demo Dekhiye:* {DEMO_SALON}

✨ *Top Features:*
1. 💄 Bridal & Pre-Bridal Package Estimator
2. 🔄 Before/After Transformation Slider
3. 📲 Direct WhatsApp Booking Hub (Zero aggregator commission)
4. 🆓 Lifetime Free Hosting (No recurring monthly fee)

Aap ek baar demo link check kijiye ma'am, agar aapko accha lage toh 24 hours me aapke rate card & photos ke sath live kar denge! 🚀

Best regards,
*Alok Lovanshi*
OmniViral Digital Studio, Bhopal
📱 Direct: +91 6265048497"""

    # Price / Cost inquiry
    if any(k in lower for k in ["price", "cost", "kharcha", "rate", "kitna", "charges", "fees", "kitne me"]):
        if any(k in lower for k in ["qr", "standee", "google review"]):
            return """Namaste Sir/Ma'am 🙏

Custom Google Maps 5★ Review Acrylic Counter Standee ka one-time setup cost sirf ₹1,499 hai.
• Lifetime Validity: Isme koi monthly charge ya subscription nahi hai.
• Direct 5★ Reviews: Client counter par phone tap/scan karke 5 second me Google par 5★ review de sakta hai.

Aap mujhe apna clinic/salon ka exact Google Maps link bhej dijiye, main sample proof ready kar dunga! 🚀"""
        else:
            return f"""Namaste Sir/Ma'am 🙏

Hamare Interactive Luxury Web Portal ka setup fee bohot hi minimal hai:
• One-time Customization & Setup: Sirf ₹4,999 (complete luxury working portal).
• Hosting & Server: LIFETIME FREE (Global Enterprise CDN architecture par hosted hai — Zero recurring monthly/annual bills, 100% free SSL security, aur unlimited visits).

Aap mujhe yahan WhatsApp par hi apni services/rate card aur 4-5 photos bhej dijiye, main 24 ghante me aapka customized preview bana kar live link bhej dunga. Preview pasand aane par hi aap aage proceed kar sakte hain! 🚀"""

    # Demo feedback / Customization inquiry
    if any(k in lower for k in ["accha", "achha", "good", "nice", "photo", "timing", "change", "hamari", "customize", "kab", "karna hai"]):
        return """Namaste Sir/Ma'am 🙏

Ji bilkul! Yeh live demo sirf ek reference blueprint tha.
Aapka exact rate card, clinic/salon ki original photos, staff details, WhatsApp number aur timing sab kuch 24 ghante ke andar accurately customize ho jayega.

Aap mujhe yahan WhatsApp par hi details bhej dijiye:
1. Clinic/Salon ka Full Name & Timing
2. Top Services & unka approximate rate
3. 3-4 interior/exterior photos

Main kal tak aapka customized live portal ready karke link share kar dunga! 🚀"""

    # Call / Meeting request
    if any(k in lower for k in ["call", "baat", "phone", "milna", "batao", "bataiye"]):
        return """Namaste Sir/Ma'am 🙏

Aapki poori requirements main yahan WhatsApp par directly handle kar raha hoon. 
Aapko kisi physical meeting ya lamba form bharne ki zaroorat nahi hai — aap mujhe yahan WhatsApp par details/photos bhej dijiye, main 24 ghante ke andar preview portal bana kar bhej dunga.

Agar koi specific urgent query hai toh aap mujhe direct WhatsApp text ya audio note bhej sakte hain, main turant answer kar dunga! 🚀"""

    # General greeting / fallback
    return f"""Namaste Sir/Ma'am 🙏

Mera naam Alok hai (Bhopal Digital Growth Studio).
Maine aapke business ke liye ek dedicated high-converting Live Demo Web Portal banaya hai:
👉 {DEMO_SALON}

Aap isme interactive packages aur WhatsApp slot booking test kar sakte hain.
Aap batayein sir, kaisa laga aapko? 🚀"""

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🤖 Autonomous Lead Responder Daemon Active...")
    processed = load_processed()

    last_size = 0
    if os.path.exists(INBOUND_LOG_PATH):
        last_size = os.path.getsize(INBOUND_LOG_PATH)

    while True:
        try:
            if os.path.exists(INBOUND_LOG_PATH):
                curr_size = os.path.getsize(INBOUND_LOG_PATH)
                if curr_size > last_size or curr_size > 0:
                    with open(INBOUND_LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        msg_hash = str(hash(line))
                        if msg_hash in processed:
                            continue

                        try:
                            item = json.loads(line)
                            chat_id = item.get("chatId", "")
                            sender_id = item.get("senderId", "")
                            text = item.get("text", "").strip()

                            # Avoid self messages or empty messages
                            if not text or "6265048497" in sender_id:
                                processed.add(msg_hash)
                                continue

                            print(f"\n⚡ NEW INBOUND MESSAGE DETECTED from {sender_id}: {text[:80]}...")
                            reply = generate_reply(text, item)

                            # Determine reply target JID
                            target_jid = chat_id if chat_id and not chat_id.endswith("@lid") else sender_id
                            
                            # If LID, check if phone number in text or look up
                            phone_in_text = get_clean_phone(text)
                            if phone_in_text:
                                target_jid = f"91{phone_in_text}@s.whatsapp.net"

                            if reply:
                                success = send_wa(target_jid, reply)
                                if success:
                                    processed.add(msg_hash)
                                    save_processed(processed)
                        except Exception as ex:
                            print(f"Error parsing line: {ex}")
                    
                    last_size = curr_size
            time.sleep(3)
        except Exception as e:
            print(f"Daemon Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
