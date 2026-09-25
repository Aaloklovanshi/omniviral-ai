import json
import random
import uuid
from backend.database import get_connection

AI_HUNT_NICHES = [
    {
        "category": "Secret / Underground AI Tools",
        "templates": [
            "3 Free AI websites that feel illegal to know in 2026...",
            "Google and Microsoft don't want you to find this AI tool...",
            "Stop paying for video editors — this free AI tool does everything in 1 click...",
            "This secret AI tool creates full 3D animated videos with zero experience..."
        ]
    },
    {
        "category": "AI Video & Seekho Creators",
        "templates": [
            "How I create viral Seekho and YouTube Shorts using Gemini Pro and Veo 3...",
            "The exact prompt formula to get photorealistic 4k AI videos every single time...",
            "Kling 1.5 vs Veo 3: Which AI video generator is actually the king in 2026?...",
            "Convert any boring text into a viral Alex Hormozi style video in 30 seconds..."
        ]
    },
    {
        "category": "AI Cashflow & Micro-SaaS",
        "templates": [
            "How college students are making ₹50,000/month using these 2 AI tools...",
            "I built an entire automated AI money system with Python in 24 hours...",
            "Top 3 AI side hustles that actually pay in India without any investment..."
        ]
    }
]

class AIHuntEngine:
    """
    Dedicated Content & Growth Engine tailored for the 'ai_hunt' channel.
    Generates high-velocity Hinglish/English video scripts, Seekho formats,
    SEO tags, thumbnails concepts, and affiliate link placeholders.
    """
    
    def generate_daily_ai_hunt_pack(self, count: int = 3) -> list:
        daily_packs = []
        
        for i in range(count):
            niche_group = AI_HUNT_NICHES[i % len(AI_HUNT_NICHES)]
            hook_idea = random.choice(niche_group["templates"])
            
            # Formulate full script for ai_hunt
            script_body = f"""[HOOK - 00:00 to 00:03]: "{hook_idea}"
[AGITATION - 00:03 to 00:10]: "Dosto agar aap bhi ghanto editing aur content creation me waste kar rahe ho, toh yeh video end tak dekhna. Kyunki yeh trick 99% creators ko nahi pata."
[THE TOOL REVELATION - 00:10 to 00:25]: "Website ka naam note kar lo — OmniViral AI. Yaha pe bas apna topic dalo, aur yeh tool aapko script, Veo 3 prompts, aur Alex Hormozi style animated subtitles sab auto generate karke de deta hai."
[PROOF & ACTION - 00:25 to 00:35]: "Maine isko test kiya and result 10x viral retention tha. Is tool ka link bio aur description me pinned hai."
[CALL TO ACTION - 00:35 to 00:40]: "Follow @ai_hunt for daily underground AI tools and comment 'PROMPT' to get the free VIP prompt pack!"""
            
            scenes = [
                {
                    "scene": 1,
                    "duration": "3s",
                    "visual": "Fast zoom on ai_hunt neon glowing logo with glitch effect",
                    "veo_prompt": "Cinematic dark room with floating neon purple AI holograms, ultra-fast dynamic zoom-in, 4k 60fps --ar 9:16",
                    "voiceover": hook_idea
                },
                {
                    "scene": 2,
                    "duration": "7s",
                    "visual": "Screen recording montage of complex timeline editing being replaced by 1 click AI button",
                    "veo_prompt": "Sleek futuristic laptop screen glowing with fast AI video rendering animations, studio lighting, depth of field --ar 9:16",
                    "voiceover": "Dosto agar aap bhi ghanto editing me waste kar rahe ho, toh yeh video miss mat karna."
                },
                {
                    "scene": 3,
                    "duration": "15s",
                    "visual": "Demonstration of the AI tool generating viral captions with glowing green highlights",
                    "veo_prompt": "Ultra-crisp 4k close up of animated kinetic typography glowing with neon lime borders on dark glassmorphism background --ar 9:16",
                    "voiceover": "Website ka naam hai OmniViral AI — script, visual prompts aur subtitles sab 10 seconds me ready."
                },
                {
                    "scene": 4,
                    "duration": "10s",
                    "visual": "Direct call to action with animated follow button and comment callout",
                    "veo_prompt": "Minimalist sleek cyber studio with purple accent lighting, floating social media badge pulsing with soft light --ar 9:16",
                    "voiceover": "Follow @ai_hunt for daily tools and comment 'PROMPT' for free access."
                }
            ]
            
            pack = {
                "id": str(uuid.uuid4()),
                "channel": "ai_hunt",
                "title": f"[AI HUNT REEL #{i+1}] {hook_idea[:45]}...",
                "category": niche_group["category"],
                "hook": hook_idea,
                "full_hinglish_script": script_body,
                "scenes": scenes,
                "thumbnail_concept": f"Big bold text: '99% DON'T KNOW THIS' + Shocked developer reaction + Neon Tool Logo",
                "youtube_title": f"{hook_idea} 🚀 (Secret AI Tools 2026) #shorts",
                "instagram_caption": f"{hook_idea}\n\nSave this reel for later! 💾\n\nFollow @ai_hunt for daily underground AI updates, prompts, and tutorials.\n\n#aihunt #aitools #aiupdates #artificialintelligence #geminipro #seekho #reelsviral #techreels #creatorgrowth #omniviral",
                "viral_score": f"{random.randint(94, 99)}/100"
            }
            daily_packs.append(pack)
            
        return daily_packs
