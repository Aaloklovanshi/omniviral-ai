"""
OmniViral AI - High-Ticket Local Business Web Agency Outreach Engine
100-Year Master Salesman Persuasion Architecture & ICP Financial Qualification Engine.
"""

import json
import os
import sys

TARGET_LEADS = [
    {
        "id": "lead_001",
        "business_name": "Shrivastava Dental Clinic & Implant Center",
        "category": "Dental & Healthcare",
        "avg_ticket_size": "₹5,000 - ₹50,000 per patient (RCT & Implants)",
        "location": "Arera Colony, Bhopal",
        "rating": 4.9,
        "review_count": 65,
        "phone": "+91 9977401234",
        "contact_person": "Dr. Shrivastava",
        "website_status": "No Dedicated Website",
        "demo_url": "https://aaloklovanshi.github.io/omniviral-ai/demos/dental_booking.html",
        "utility_tool": "24/7 Automated Patient Slot Selector & WhatsApp Intake Hub",
        "roi_proof": "Just 1 Root Canal treatment (₹5,000) pays for the entire website 3x over!"
    },
    {
        "id": "lead_002",
        "business_name": "Art Link Interiors",
        "category": "Interior Design & Architecture",
        "avg_ticket_size": "₹2,00,000 - ₹15,00,000 per project",
        "location": "E8 Arera Colony, Bhopal",
        "rating": 4.9,
        "review_count": 38,
        "phone": "+91 9425018921",
        "contact_person": "Lead Architect",
        "website_status": "Outdated 2010s Profile",
        "demo_url": "https://aaloklovanshi.github.io/omniviral-ai/demos/interior_calculator.html",
        "utility_tool": "Instant 3D Room Quotation & Renovation Cost Estimator",
        "roi_proof": "1 extra 3BHK interior contract (₹5 Lakhs+) gives 150x ROI!"
    },
    {
        "id": "lead_003",
        "business_name": "METROMEN Unisex Salon & Spa",
        "category": "Premium Salon & Grooming",
        "avg_ticket_size": "₹2,000 - ₹12,000 (Keratin & VIP Packages)",
        "location": "MP Nagar, Bhopal",
        "rating": 5.0,
        "review_count": 45,
        "phone": "+91 8815949846",
        "contact_person": "Salon Director",
        "website_status": "No Website (Relies on WhatsApp Catalog)",
        "demo_url": "https://aaloklovanshi.github.io/omniviral-ai/demos/dental_booking.html",
        "utility_tool": "VIP Package Menu & Stylist Slot Booking Portal",
        "roi_proof": "2 VIP Salon packages per month pay for the complete site!"
    },
    {
        "id": "lead_004",
        "business_name": "Amyra Beauty Junction & Bridal Studio",
        "category": "Bridal & Beauty Studio",
        "avg_ticket_size": "₹15,000 - ₹45,000 per bridal booking",
        "location": "Piplani, Bhopal",
        "rating": 4.8,
        "review_count": 82,
        "phone": "+91 9752461221",
        "contact_person": "Studio Manager",
        "website_status": "No Website",
        "demo_url": "https://aaloklovanshi.github.io/omniviral-ai/demos/dental_booking.html",
        "utility_tool": "Bridal Package Gallery & Direct Slot Reservation System",
        "roi_proof": "1 Bridal makeup booking (₹20k) pays for the website 7x over!"
    }
]

def generate_master_salesman_whatsapp(lead: dict) -> str:
    """100-Year Master Salesman Script for WhatsApp outreach."""
    name = lead['business_name']
    rating = lead['rating']
    reviews = lead['review_count']
    cat = lead['category']
    demo = lead['demo_url']
    tool = lead['utility_tool']
    roi = lead['roi_proof']
    
    msg = f"""Namaste Sir/Ma'am 🙏

Mera naam Alok hai (Bhopal Digital Growth Agency). 

Maine Google Maps par **{name}** dekha. Aapki **{rating}★ Rating ({reviews}+ Reviews)** bohot hi impressive hai! 👏 Local Bhopal me log aapki quality ko bohot admire karte hain.

Lekin ek critical detail jo aapka har mahine **₹30,000+ ka revenue loss** karwa rahi hai:

🚫 Jab koi patient/client Google par search karta hai, aapki koi **Official Utility Website** nahi hai.

💡 **Word of Mouth vs Digital Reality:**
Aap soch rahe honge: *"Humari rating achhi hai, log waise hi aate hain."*
Lekin Google data dikhata hai ki **70% Word-of-Mouth leads pehle Google par search karke credibility check karte hain.** Website na milne par 4 out of 10 leads competitors ke paas chale jaate hain.

🔥 **Humne aapke business ke liye ek Live Interactive Utility Website (Demo) bana di hai:**
👉 **Live Demo Test Link:** {demo}

✨ **Yeh Simple Brochure Website Nahi Hai — Yeh Aapka Kaam Asaan Karegi:**
✅ **{tool}**
✅ Reception par phone calls ka load 50% kaam hoga.
✅ Raat ko 9 PM ke baad bhi log appointment/inquiry book kar sakte hain.

💰 **Complete Expense & 10x ROI Breakdown:**
• Domain Name: ~₹499/year (Direct your name)
• Hosting & Server: **₹0 / LIFETIME FREE** (Zero recurring monthly bills)
• Setup & Customization: Sirf **₹1,499 (One-Time)**
👉 **{roi}**

🛡️ **100% Risk-Free Guarantee:** 
Hum 48 hours me aapki complete website live karke denge. Agar aapko pasand na aaye, toh 100% refund. No questions asked.

Kya hum 2 minute baat kar sakte hain? Aap live demo link open karke test kar lijiye! 🚀

Best regards,
**Alok Lovanshi**  
OmniViral / Digital Growth Studio  
📱 Direct WhatsApp: +91 6265048497
"""
    return msg

def generate_master_salesman_email(lead: dict) -> str:
    """100-Year Master Salesman Executive Email Proposal."""
    name = lead['business_name']
    rating = lead['rating']
    cat = lead['category']
    demo = lead['demo_url']
    tool = lead['utility_tool']
    roi = lead['roi_proof']
    ticket = lead['avg_ticket_size']
    
    subject = f"Executive Web Proposal: Live Utility Demo for {name} ({rating}★ Google Rated)"
    
    body = f"""Subject: {subject}

Dear Management Team at {name},

My name is Alok Lovanshi, Founder at OmniViral Digital Agency based in Bhopal.

While conducting an operational digital audit of top-tier {cat} providers in Bhopal, your profile for **{name}** stood out with an exceptional **{rating}-Star Google Rating**.

However, we noticed a critical operational gap: **{name} does not currently have an Official Utility Web Portal.**

---

### 📉 The Hidden Cost of Not Having an Official Utility Website:
1. **The Word-of-Mouth Leak:** Even when a client is recommended to you by word-of-mouth, 70% look you up on Google first. Without a professional web utility, 40% of those pre-qualified leads drop off to competitors.
2. **After-Hours Opportunity Loss:** Over 45% of appointment searches occur after business hours (between 8:00 PM and 11:00 PM). Without an online booking engine, these inquiries are lost forever.

---

### 💻 We Have Built a Live Utility Demo Specifically For Your Business:
Instead of explaining in words, we built a live working preview for you:
🔗 **Test the Live Demo Here:** {demo}

**What This Web Application Does For You:**
- **{tool}**
- Direct WhatsApp & Email Instant Booking Notifications.
- 100% Mobile Responsive & Ultra-Fast Loading (Sub-second speed).

---

### 📊 Transparent Expense & Investment Breakdown:
We believe in 100% pricing clarity with ZERO hidden monthly costs:
- **Domain Registration:** ~₹499 / year (Registered under your ownership).
- **Cloud Hosting & SSL Security:** **₹0 / LIFETIME FREE** (Hosted on high-speed CDN with zero recurring monthly server fees).
- **Custom Development & Setup:** **₹1,499** (One-Time Professional Fee).

💰 **The ROI Math:**
Average Ticket Size: {ticket}.  
👉 **{roi}**

---

### 🤝 100% Zero-Risk Execution Guarantee:
We deliver your fully customized, production-ready website within **48 Hours**. If you are not 100% satisfied with the design and utility, you pay ZERO.

Would you be open for a quick 3-minute phone or WhatsApp conversation today?

Warm regards,

**Alok Lovanshi**  
Founder & Technical Lead | OmniViral Studio  
📞 Direct Phone / WhatsApp: +91 6265048497  
✉️ Email: freeediting35@gmail.com  
🌐 Live Portfolio: https://aaloklovanshi.github.io/omniviral-ai/
"""
    return body

def export_all_master_leads():
    """Exports all target leads with master salesman pitches."""
    out_dir = "marketing/outreach_leads"
    os.makedirs(out_dir, exist_ok=True)
    
    processed = []
    md_content = "# 🏆 100-Year Master Salesman High-Ticket Outreach Directory\n\n"
    md_content += "Targeting high-ticket local businesses in Bhopal with 4.8+ Google Rating.\n\n"
    
    for idx, lead in enumerate(TARGET_LEADS, 1):
        wa_pitch = generate_master_salesman_whatsapp(lead)
        email_pitch = generate_master_salesman_email(lead)
        
        lead_entry = {
            **lead,
            "whatsapp_pitch": wa_pitch,
            "email_pitch": email_pitch
        }
        processed.append(lead_entry)
        
        md_content += f"## {idx}. {lead['business_name']} ({lead['rating']}★ - {lead['review_count']} Reviews)\n"
        md_content += f"- **Category:** {lead['category']}\n"
        md_content += f"- **Average Ticket Size:** {lead['avg_ticket_size']}\n"
        md_content += f"- **Phone / WhatsApp:** `{lead['phone']}`\n"
        md_content += f"- **Live Demo Link:** [{lead['demo_url']}]({lead['demo_url']})\n"
        md_content += f"- **Utility Value:** {lead['utility_tool']}\n"
        md_content += f"- **ROI Proof:** {lead['roi_proof']}\n\n"
        md_content += "### 💬 WhatsApp Master Salesman Pitch:\n```text\n" + wa_pitch + "\n```\n\n"
        md_content += "### ✉️ Executive Email Proposal:\n```text\n" + email_pitch + "\n```\n\n"
        md_content += "---\n\n"
        
    with open(f"{out_dir}/google_maps_leads.json", "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
        
    with open(f"{out_dir}/outreach_master_playbook.md", "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"✅ Master Salesman Engine updated successfully with {len(processed)} qualified leads!")

if __name__ == "__main__":
    export_all_master_leads()
