import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import uuid

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output" / "thumbnails"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ThumbnailEngine:
    """
    Automatically generates high-CTR (Click-Through Rate) vertical cover thumbnails
    for YouTube Shorts, Instagram Reels, and TikTok.
    """
    def __init__(self, width: int = 720, height: int = 1280):
        self.width = width
        self.height = height

    def generate_high_ctr_cover(self, title_main: str, highlight_word: str, filename: str) -> str:
        # Create base dark gradient layer
        img = Image.new("RGB", (self.width, self.height), color=(15, 10, 25))
        draw = ImageDraw.Draw(img)

        # Draw diagonal neon accent lines
        draw.line([0, self.height, self.width, 0], fill=(139, 92, 246), width=8)
        draw.line([0, self.height - 200, self.width, -200], fill=(236, 72, 153), width=4)

        # Draw a glowing center focal point for "Viral Retention"
        center_y = self.height // 2 - 100
        center_x = self.width // 2
        
        # Center glow ellipse
        for radius in range(300, 50, -20):
            glow = int((300 - radius) / 300 * 255)
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                fill=(245, 158, 11, glow // 5)
            )

        # Main Title (Shock/Curiosity factor) -> E.g., "99% WRONG" or "SECRET AI TOOL"
        title_y = center_y - 250
        
        # Draw background shadow for text pop
        draw.rectangle([50, title_y - 80, self.width - 50, title_y + 80], fill=(225, 29, 72), outline=(255, 255, 255), width=4)
        draw.text((self.width // 2, title_y), title_main.upper(), fill=(255, 255, 255), anchor="mm")

        # Highlight box for the Hook word (e.g. "STOP SCROLLING" or "SECRET")
        highlight_y = title_y + 180
        draw.rectangle([self.width//2 - 250, highlight_y - 60, self.width//2 + 250, highlight_y + 60], fill=(34, 197, 94))
        draw.text((self.width // 2, highlight_y), highlight_word.upper(), fill=(0, 0, 0), anchor="mm")

        # Bottom Call To Action / Branding
        draw.rectangle([0, self.height - 120, self.width, self.height], fill=(0, 0, 0))
        draw.text((self.width // 2, self.height - 60), "🔥 @ai_hunt OFFICIAL", fill=(139, 92, 246), anchor="mm")

        # Save output
        out_path = Path(filename)
        if not out_path.is_absolute():
            out_path = OUTPUT_DIR / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="JPEG", quality=95)
        return str(out_path)

if __name__ == "__main__":
    t = ThumbnailEngine()
    print("Thumbnail generated at:", t.generate_high_ctr_cover("99% Creators Fail At This", "SECRET TOOL", "sample_cover.jpg"))