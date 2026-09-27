import sys
import send_wa as wa

text = """Namaste Sir 🙏

Bilkul, maine dekha tha ki aapka MP Nagar me *METROMEN Salon* bohot reputed hai aur Google par *5.0★ Perfect Rating* hai, lekin official high-converting website nahi thi — sirf Justdial/Magicpin listings thi.

Aapke salon ke prestige aur standard ko dekh kar humne specifically **METROMEN Luxury Salon & Spa** ke liye dedicated Live VIP Web Application tayyar kiya hai!

👉 *Live Demo Link Dekhiye:*
https://aaloklovanshi.github.io/omniviral-ai/demo_salon.html

✨ *Is Application ke Top Features:*
1. 💇♂️ *Instant Package & Service Estimator:* Client haircut, keratin, hydra-facial select karke online bill estimate calculate kar sakta hai.
2. 🔄 *Before & After Transformation Slider:* Grooming transformations live dekhne ke liye interactive visual slider.
3. 📲 *Direct WhatsApp VIP Chair Booking:* Client seedhe aapke WhatsApp number (+91 8815949846) par bina kisi aggregator commission ke booking bhej sakta hai!
4. 🆓 *Zero Monthly Server Cost:* Hosting lifetime free hai.

Aap ek baar demo link open karke apne phone me test kijiye sir! Agar aapko pasand aaye toh hum isme aapka exact rate chart aur images set karke 24 ghante me live kar denge. 🚀

Best regards,
*Alok Lovanshi*
OmniViral Digital Studio, Bhopal
📱 Direct WhatsApp: +91 6265048497"""

res = wa.send_whatsapp_message("8815949846", text)
print("Result:", res)
