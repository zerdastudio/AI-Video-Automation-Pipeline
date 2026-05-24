import json, sys, re

def format_timestamp(seconds):
    h = int(seconds // 3600); m = int((seconds % 3600) // 60); s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

audio_in = sys.argv[1]
fixes_file = sys.argv[2]
json_in = audio_in.rsplit(".", 1)[0] + ".json"
ass_file = audio_in.rsplit(".", 1)[0] + ".ass"

with open(fixes_file, "r", encoding="utf-8-sig") as f:
    fixes = json.load(f)

with open(json_in, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

COLOR_MAP = {
    "MAMMA": "&H9314FF&", "POPPATA": "&H9314FF&",
    "FERMATI": "&H0024FF&", "NIENTE": "&H0024FF&", "NESSUNO": "&H0024FF&", "MINUTI": "&H0024FF&",
    "CAMBIARE": "&H14FF39&", "COSE": "&H14FF39&", "SOLDI": "&H14FF39&",
    "TUO": "&H00D7FF&", "GUADAGNATO": "&H00D7FF&", "PROGETTO": "&H00D7FF&", "SUO": "&H00D7FF&", "CENTINAIA": "&H00D7FF&",
    "CASA": "&HFFBF00&", "RIPOSINO": "&HFFBF00&",
    "DONNA": "&HE22B8A&"
}

DEFAULT_HIGHLIGHT = "&H00FFFF&" # Giallo neon per le parole parlate non in lista
MAX_WORDS = 4 # Numero massimo di parole a schermo per farci stare il Font 140

ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Impact,140,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,12,6,2,10,10,350,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

lines = [ass_header]

# Crea blocchi dinamici al millisecondo
for segment in data.get("segments", []):
    words = [w for w in segment.get("words", []) if "start" in w]
    
    # Se per qualche motivo la lista è vuota, salta il blocco
    if not words:
        continue

    # Suddivide la frase in blocchi (es. 4 parole alla volta)
    for i in range(0, len(words), MAX_WORDS):
        chunk = words[i:i+MAX_WORDS]
        
        # Per ogni parola nel blocco, creiamo il frame in cui E' ACCESA
        for k in range(len(chunk)):
            active_word = chunk[k]
            start_time = format_timestamp(active_word["start"])
            
            # La parola si spegne quando inizia la successiva, o quando finisce se è l'ultima
            if k < len(chunk) - 1:
                end_time = format_timestamp(chunk[k+1]["start"])
            else:
                end_time = format_timestamp(active_word["end"])
                
            display_words = []
            for j, w in enumerate(chunk):
                clean_w = w["word"].strip()
                for wrong, right in fixes.items():
                    clean_w = re.sub(rf"\b{wrong}\b", right, clean_w, flags=re.IGNORECASE)
                clean_w = clean_w.upper()
                
                # Se è la parola che sta pronunciando ORA, accendila
                if j == k: 
                    check_word = re.sub(r'[^\w\s]', '', clean_w)
                    highlight = DEFAULT_HIGHLIGHT
                    for keyword, hex_color in COLOR_MAP.items():
                        if keyword in check_word:
                            highlight = hex_color
                            break
                    display_words.append(f"{{\\c{highlight}}}{clean_w}{{\\c&HFFFFFF&}}")
                # Le altre parole restano spente (bianche)
                else: 
                    display_words.append(f"{{\\c&HFFFFFF&}}{clean_w}")
                    
            final_text = " ".join(display_words)
            lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{final_text}\n")

with open(ass_file, "w", encoding="utf-8-sig") as f:
    f.writelines(lines)
