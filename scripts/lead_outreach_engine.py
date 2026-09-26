"""
OmniViral AI - High-Rated Local Business Website Outreach Engine
Targeting high-rated Google Maps businesses (4.8 - 5.0 Stars) that lack dedicated websites.
Generates personalized WhatsApp & Email sales pitches to close web design clients.
"""

import json
import os
import sys

TARGET_LEADS = [
    {
        "id": "lead_001",
        "business_name": "Shrivastava Dental Clinic & Implant Center",
        "category": "Dental Clinic / Healthcare",
        "location": "Bhopal, MP",
        "rating": 4.9,
        "review_count": 65,
        "phone": "+91 9977401234",
        "contact_person": "Dr. Shrivastava",
        "website_status": "No Dedicated Website (Only Google Maps listing)",
        "pain_point": "Patients can't book appointments online or view before/after smile transformations.",
        "pitch_angle": "Instant Online Appointment Booking & 24/7 Patient Trust Hub"
    },
    {
        "id": "lead_002",
        "business_name": "METROMEN Unisex Salon & Spa",
        "category": "Salon & Grooming",
        "location": "Arera Colony / MP Nagar, Bhopal",
        "rating": 5.0,
        "review_count": 45,
        "phone": "+91 8815949846",
        "contact_person": "Salon Manager",
        "website_status": "No Website (Relies on WhatsApp Catalog & Reels)",
        "pain_point": "Losing high-paying client bookings to chains like Naturals & Lakme who have online portals.",
        "pitch_angle": "VIP Service Catalog & Direct Slot Booking Website"
    },
    {
        "id": "lead_003",
        "business_name": "Amyra Beauty Junction & Salon",
        "category": "Beauty & Bridal Studio",
        "location": "Piplani / MP Nagar, Bhopal",
        "rating": 4.8,
        "review_count": 82,
        "phone": "+91 9752461221",
        "contact_person": "Owner / Manager",
        "website_status": "No Website (Listed on local directory only)",
        "pain_point": "Bridal makeup packages missing custom online booking & portfolio showcase.",
        "pitch_angle": "Bridal Package Showcase & Direct Lead Generation Website"
    },
    {
        "id": "lead_004",
        "business_name": "Art Link Interiors",
        "category": "Interior Design & Contracting",
        "location": "E8 Arera Colony, Bhopal",
        "rating": 4.9,
        "review_count": 38,
        "phone": "+91 9425018921",
        "contact_person": "Lead Architect / Designer",
        "website_status": "Outdated landing page (No interactive project calculator or portfolio)",
        "pain_point": "High-budget home owners demand modern 3D portfolio & online consultation booking.",
        "pitch_angle": "Luxury Interior Portfolio & Instant Quotation Calculator Site"
    },
    {
        "id": "lead_005",
        "business_name": "Kookie Kids Salon & Makeup Studio",
        "category": "Kids & Family Grooming",
        "location": "E3 Arera Colony, Bhopal",
        "rating": 4.8,
        "review_count": 54,
        "phone": "+91 9826249229",
        "contact_person": "Studio Director",
        "website_status": "No Website (Local directory only)",
        "pain_point": "Parents prefer viewing hygienic kids' grooming packages online before visiting.",
        "pitch_angle": "Interactive Package Menu & Family Appointment Website"
    },
    {
        "id": "lead_006",
        "business_name": "Tathastu Dental Care",
        "category": "Multi-Speciality Dental Hospital",
        "location": "Hoshangabad Road, Bhopal",
        "rating": 5.0,
        "review_count": 95,
        "phone": "+91 7869012345",
        "contact_person": "Dr. Pathak / Manager",
        "website_status": "No Website (Only Google Business Profile)",
        "pain_point": "Google Maps searchers select competitors who have official website links.",
        "pitch_angle": "NABH-Style High-Trust Dental Portal with Patient Reviews"
    }
]

def generate_whatsapp_pitch(lead: dict) -> str:
    """Generates a high-converting, friendly Hinglish WhatsApp pitch for the business owner."""
    name = lead['business_name']
    rating = lead['rating']
    reviews = lead['review_count']
    cat = lead['category']
    angle = lead['pitch_angle']
    
    msg = f"""Namaste Sir/Ma'am 🙏

Mera naam Alok hai (Bhopal Digital Growth Agency). 

Maine Google Maps par aapki **{name}** dekhi. Aapki **{rating}★ Rating ({reviews}+ Reviews)** sach me outstanding hai! 👏 Local Bhopal me log aapki service ko bohot pasand karte hain.

Lekin maine notice kiya ki jab koi Google par search karta hai, toh aapki koi **Official Website** nahi hai (ya direct booking portal link nahi hai).

💡 **Aapko pata hai?**
Google par har mahine **3,000+ log Bhopal me {cat}** search karte hain. Website na hone ki wajah se 40% high-paying customers un competitors ke paas chale jaate hain jinki website hoti hai.

🔥 **Hum aapke liye ek Super Fast Modern Website bana sakte hain jisme:**
✅ Instant Online Appointment / Slot Booking System
✅ Premium Photo Gallery & Client Reviews Showcase
✅ WhatsApp Direct Chat & Call Buttons
✅ 100% Mobile Fast & Google Search SEO Ready

💰 **Special Bhopal Business Offer:**
Aapko hum **Complete Website + FREE Hosting + Domain setup** sirf 48 hours me ready karke denge.

Kya hum 2 minute WhatsApp message par connect kar sakte hain? Main aapko ek **FREE Sample Demo Website** ka preview link bhej deta hoon! 🚀

Best regards,
**Alok Lovanshi**
OmniViral / Digital Growth Studio
📱 WhatsApp: +91 6265048497
"""
    return msg

def generate_email_pitch(lead: dict) -> str:
    """Generates a professional, value-packed proposal email for business decision makers."""
    name = lead['business_name']
    rating = lead['rating']
    cat = lead['category']
    
    subject = f"Proposal: Official High-Converting Website for {name} ({rating}★ Google Rated)"
    
    body = f"""Subject: {subject}

Dear Management Team at {name},

I hope this email finds you well.

My name is Alok Lovanshi, Founder at OmniViral Digital Studio based in Bhopal. 

While auditing top-rated local businesses in Bhopal, your profile for **{name}** stood out remarkably with an impressive **{rating}-Star Google Rating**. Your customer satisfaction is clearly among the best in the city.

However, we observed that potential clients searching for top-tier **{cat}** on Google search cannot currently access an **Official Website** for your business.

---

### 🚨 Why Having No Official Website is Costing You Clients Every Month:

1. **Lost Search Traffic:** Over 70% of high-ticket clients search on Google first. Without a website, searchers automatically navigate to competitors who provide an immediate website link.
2. **No Instant Booking System:** High-value customers prefer booking appointments online outside business hours (late evenings & early mornings).
3. **Credibility & Premium Brand Positioning:** A modern 24/7 web portal elevates your brand positioning from a "local shop" to a premium market leader in Bhopal.

---

### 🚀 What We Will Build For {name}:

- **Custom-Designed Modern Website:** 100% mobile-responsive, dark/light glassmorphic UI.
- **Direct Online Booking & Inquiry System:** Connected straight to your WhatsApp and email.
- **Service Catalog & Before/After Showcase:** Highlight your premium offerings with high CTR.
- **Google Maps & Local SEO Integration:** Rank #1 in local search results across Bhopal.
- **Ultra-Fast Performance & Free Hosting:** SSL Secured (HTTPS) with zero maintenance headache.

---

### 🎁 Limited-Time Executive Offer for Bhopal Businesses:
We deliver full turn-key website setups within **48 Hours** with **Zero Technical Hassle** on your end.

We would love to share a **Live Interactive Demo Website Template** customized for {name}. 

Would you be open for a quick 5-minute discussion on phone or WhatsApp?

Warm regards,

**Alok Lovanshi**  
Founder & Director | OmniViral Digital Agency  
📞 Direct Phone / WhatsApp: +91 6265048497  
✉️ Email: freeediting35@gmail.com  
🌐 Portfolio: https://aaloklovanshi.github.io/omniviral-ai/
"""
    return body

def export_all_leads():
    """Exports all target leads with generated pitches to JSON and Markdown format."""
    out_dir = "marketing/outreach_leads"
    os.makedirs(out_dir, exist_ok=True)
    
    processed = []
    md_content = "# 🎯 High-Rated Google Maps Business Outreach Master Directory\n\n"
    md_content += "Targeting businesses in Bhopal with 4.8+ Google Rating lacking dedicated websites.\n\n"
    
    for idx, lead in enumerate(TARGET_LEADS, 1):
        wa_pitch = generate_whatsapp_pitch(lead)
        email_pitch = generate_email_pitch(lead)
        
        lead_entry = {
            **lead,
            "whatsapp_pitch": wa_pitch,
            "email_pitch": email_pitch
        }
        processed.append(lead_entry)
        
        md_content += f"## {idx}. {lead['business_name']} ({lead['rating']}★ - {lead['review_count']} Reviews)\n"
        md_content += f"- **Category:** {lead['category']}\n"
        md_content += f"- **Location:** {lead['location']}\n"
        md_content += f"- **Phone / WhatsApp:** `{lead['phone']}`\n"
        md_content += f"- **Status:** {lead['website_status']}\n"
        md_content += f"- **Pitch Strategy:** {lead['pitch_angle']}\n\n"
        md_content += "### 💬 WhatsApp Pitch (Hinglish High-CTR):\n```text\n" + wa_pitch + "\n```\n\n"
        md_content += "### ✉️ Email Pitch Proposal:\n```text\n" + email_pitch + "\n```\n\n"
        md_content += "---\n\n"
        
    with open(f"{out_dir}/google_maps_leads.json", "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
        
    with open(f"{out_dir}/outreach_master_playbook.md", "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"✅ Successfully exported {len(processed)} high-rated leads and pitches to {out_dir}!")

if __name__ == "__main__":
    export_all_leads()
