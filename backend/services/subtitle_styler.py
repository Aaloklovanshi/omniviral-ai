import math

class SubtitleEngine:
    """
    Generates high-engagement animated karaoke-style subtitles.
    Supports:
    - ASS (Advanced SubStation Alpha) for native FFmpeg / CapCut / Premiere styling
    - SRT format for universal YouTube/Instagram upload
    - JSON Timeline with word-level highlight timestamps
    """
    
    STYLE_PRESETS = {
        "hormozi_bold": {
            "name": "Alex Hormozi Viral Bold",
            "font": "THE BOLD FONT, Montserrat, Arial Black",
            "font_size": 48,
            "primary_color": "&H00FFFFFF",  # White
            "highlight_color": "&H0000FF00", # Neon Green / Lime
            "secondary_highlight": "&H0000FFFF", # Neon Yellow
            "outline_color": "&H00000000",  # Deep Black outline
            "outline_width": 4,
            "shadow_depth": 2,
            "uppercase": True
        },
        "beast_pop": {
            "name": "MrBeast Dynamic Pop",
            "font": "Komika Axis, Impact, Arial",
            "font_size": 52,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H0000A5FF", # Bright Orange
            "secondary_highlight": "&H00FF00FF", # Magenta
            "outline_color": "&H00000000",
            "outline_width": 5,
            "shadow_depth": 3,
            "uppercase": True
        },
        "minimal_clean": {
            "name": "Minimalist Cyberpunk Clean",
            "font": "Inter, Geist, Helvetica",
            "font_size": 40,
            "primary_color": "&H00F0F0F0",
            "highlight_color": "&H00FF7F00", # Electric Cyan
            "secondary_highlight": "&H00FFFFFF",
            "outline_color": "&H00111111",
            "outline_width": 2,
            "shadow_depth": 1,
            "uppercase": False
        }
    }

    def generate_timed_subtitles(self, script_text: str, total_duration: float = 30.0, preset: str = "hormozi_bold") -> dict:
        words = script_text.strip().split()
        if not words:
            return {"srt": "", "ass": "", "json_timeline": []}
            
        time_per_word = total_duration / max(1, len(words))
        
        # Group into 2 to 4 words per subtitle chunk
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        json_timeline = []
        srt_lines = []
        ass_dialogues = []
        
        current_time = 0.0
        
        for idx, chunk in enumerate(chunks):
            chunk_duration = len(chunk) * time_per_word
            start_t = current_time
            end_t = current_time + chunk_duration
            
            chunk_text = " ".join(chunk)
            if preset in ["hormozi_bold", "beast_pop"]:
                chunk_text = chunk_text.upper()
                
            # Random or heuristic power-word highlight (usually first or last word in chunk)
            highlight_index = len(chunk) - 1
            highlighted_word = chunk[highlight_index]
            
            # 1. JSON Timeline Representation
            json_timeline.append({
                "id": idx + 1,
                "start": round(start_t, 2),
                "end": round(end_t, 2),
                "text": chunk_text,
                "words": [
                    {
                        "word": w.upper() if preset in ["hormozi_bold", "beast_pop"] else w,
                        "highlight": (i == highlight_index),
                        "start": round(start_t + (i * time_per_word), 2),
                        "end": round(start_t + ((i + 1) * time_per_word), 2)
                    }
                    for i, w in enumerate(chunk)
                ]
            })
            
            # 2. SRT Format
            srt_start = self._format_srt_time(start_t)
            srt_end = self._format_srt_time(end_t)
            srt_lines.append(f"{idx + 1}\n{srt_start} --> {srt_end}\n{chunk_text}\n")
            
            # 3. ASS Format (Karaoke style)
            ass_start = self._format_ass_time(start_t)
            ass_end = self._format_ass_time(end_t)
            # ASS with highlight color tag for the active word
            formatted_words = []
            for i, w in enumerate(chunk):
                display_w = w.upper() if preset in ["hormozi_bold", "beast_pop"] else w
                if i == highlight_index:
                    formatted_words.append(r"{\c&H0000FF00\t(0,200,\fscx115\fscy115)}" + display_w + r"{\r}")
                else:
                    formatted_words.append(display_w)
            ass_text = " ".join(formatted_words)
            ass_dialogues.append(f"Dialogue: 0,{ass_start},{ass_end},Default,,0,0,0,,{ass_text}")
            
            current_time = end_t
            
        ass_full = self._build_full_ass(ass_dialogues, preset)
        srt_full = "\n".join(srt_lines)
        
        return {
            "preset": preset,
            "total_chunks": len(chunks),
            "srt": srt_full,
            "ass": ass_full,
            "json_timeline": json_timeline
        }

    def _format_srt_time(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - math.floor(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    def _format_ass_time(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds - math.floor(seconds)) * 100)
        return f"{hrs:01d}:{mins:02d}:{secs:02d}.{centis:02d}"

    def _build_full_ass(self, dialogues: list, preset_key: str) -> str:
        p = self.STYLE_PRESETS.get(preset_key, self.STYLE_PRESETS["hormozi_bold"])
        header = f"""[Script Info]
Title: OmniViral AI Auto Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{p['font']},{p['font_size']},{p['primary_color']},{p['highlight_color']},{p['outline_color']},&H80000000,-1,0,0,0,100,100,0,0,1,{p['outline_width']},{p['shadow_depth']},2,50,50,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        return header + "\n".join(dialogues)
