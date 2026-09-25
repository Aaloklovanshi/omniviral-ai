import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

class VideoRenderer:
    """
    Renders 9:16 high-retention vertical short videos with animated kinetic typography,
    Hormozi-style neon highlights, dynamic gradient backgrounds, and progress bars.
    """
    def __init__(self, width: int = 720, height: int = 1280, fps: int = 24):
        self.width = width
        self.height = height
        self.fps = fps

    def create_gradient_frame(self, t: float, total_duration: float, title: str, active_word: str, full_phrase: str, progress: float) -> np.ndarray:
        # Create dynamic animated gradient background
        img = Image.new("RGB", (self.width, self.height), color=(10, 10, 18))
        draw = ImageDraw.Draw(img)

        # Dynamic floating ambient orbs
        center_x = int(self.width / 2 + np.sin(t * 2) * 100)
        center_y = int(self.height / 3 + np.cos(t * 2) * 80)
        radius = 280
        
        # Subtle glow circles
        draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=(30, 20, 50))
        draw.ellipse([center_x - radius // 2, center_y - radius // 2, center_x + radius // 2, center_y + radius // 2], fill=(50, 25, 80))

        # Top Badge: @ai_hunt Official
        badge_text = "🔥 @ai_hunt OFFICIAL • SECRET AI TOOLS"
        try:
            font_badge = ImageFont.load_default()
        except:
            font_badge = None
        
        # Header banner
        draw.rectangle([40, 60, self.width - 40, 120], fill=(22, 22, 34), outline=(139, 92, 246), width=2)
        draw.text((self.width // 2, 90), badge_text, fill=(245, 158, 11), anchor="mm")

        # Main Title Box
        draw.text((self.width // 2, 320), title.upper(), fill=(255, 255, 255), anchor="mm")

        # Center Video Mockup / Animation Card
        card_w, card_h = 600, 360
        card_x0, card_y0 = (self.width - card_w) // 2, 420
        draw.rectangle([card_x0, card_y0, card_x0 + card_w, card_y0 + card_h], fill=(15, 15, 25), outline=(6, 182, 212), width=3)
        
        # Pulsing AI graphic in center card
        pulse = abs(np.sin(t * 3))
        p_radius = int(60 + pulse * 25)
        cx, cy = self.width // 2, card_y0 + card_h // 2
        draw.ellipse([cx - p_radius, cy - p_radius, cx + p_radius, cy + p_radius], fill=(139, 92, 246, 120), outline=(255, 255, 255), width=2)
        draw.text((cx, cy), "⚡ AI ENGINE", fill=(255, 255, 255), anchor="mm")

        # Hormozi Style Dynamic Subtitle Box
        sub_y = 900
        words = full_phrase.split()
        
        # Draw full phrase with highlighted word
        draw.rectangle([30, sub_y - 45, self.width - 30, sub_y + 45], fill=(0, 0, 0), outline=(34, 197, 94), width=3)
        draw.text((self.width // 2, sub_y), full_phrase.upper(), fill=(34, 197, 94) if active_word in full_phrase else (255, 255, 255), anchor="mm")

        # Bottom Progress Bar
        bar_y = self.height - 40
        draw.rectangle([40, bar_y, self.width - 40, bar_y + 8], fill=(40, 40, 50))
        draw.rectangle([40, bar_y, int(40 + (self.width - 80) * progress), bar_y + 8], fill=(139, 92, 246))

        return np.array(img)

    def render_short_video(self, topic: str, hook: str, filename: str = "ai_hunt_sample_short.mp4", duration: float = 6.0) -> str:
        """
        Renders an actual 9:16 short MP4 video clip with animated visuals and subtitles.
        """
        import moviepy as mp

        output_path = OUTPUT_DIR / filename
        total_frames = int(duration * self.fps)

        phrases = [
            (0.0, 2.0, "STOP SCROLLING!"),
            (2.0, 4.0, "THIS SECRET AI TOOL"),
            (4.0, duration, "WILL 10X YOUR CONTENT!")
        ]

        def make_frame(t):
            # Find active phrase
            curr_phrase = phrases[-1][2]
            for start, end, text in phrases:
                if start <= t < end:
                    curr_phrase = text
                    break
            
            progress = min(1.0, max(0.0, t / duration))
            return self.create_gradient_frame(
                t=t,
                total_duration=duration,
                title=topic[:30],
                active_word=curr_phrase.split()[0],
                full_phrase=curr_phrase,
                progress=progress
            )

        clip = mp.VideoClip(make_frame, duration=duration)
        clip.write_videofile(
            str(output_path),
            fps=self.fps,
            codec="libx264",
            preset="ultrafast",
            logger=None
        )
        clip.close()

        return str(output_path)
