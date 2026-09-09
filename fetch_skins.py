import urllib.request
import json
import time
import sys

CATEGORIES = [
    "knight", "ninja", "dragon", "warrior", "mage", "wizard",
    "robot", "pirate", "samurai", "cyberpunk", "hacker", "astronaut",
    "demon", "angel", "king", "assassin", "viking", "soldier",
    "phantom", "creeper", "enderman", "zombie", "fox", "wolf",
    "paladin", "hunter", "archer", "reaper"
]

BLOCKED_WORDS = [
    "nude", "nuda", "nudo", "naked", "nsfw", "lewd", "hentai", "ecchi", "porn", "porno",
    "xxx", "sex", "sexy", "sexual", "erotic", "erotica", "onlyfans", "topless",
    "bottomless", "underwear", "lingerie", "bikini", "swimsuit", "desnud", "tetas",
    "teta", "culo", "vagina", "penis", "pene", "boob", "breast", "nipple", "genital",
    "futa", "loli", "shota", "r34", "rule34", "waifu nsfw", "hot girl", "hot boy"
]

def is_clean_name(name):
    if not name or len(name.strip()) < 2:
        return False
    lower = name.lower()
    for w in BLOCKED_WORDS:
        if w in lower:
            return False
    return True

def fetch_skins():
    unique_skins = []
    seen_urls = set()
    target_count = 210

    print(f"Buscando hasta {target_count} skins populares...")

    for cat in CATEGORIES:
        if len(unique_skins) >= target_count:
            break
        url = f"https://api.mineskin.org/get/list/0?filter={cat}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WebcraftSkinFetcher/1.0"})
            with urllib.request.urlopen(req, timeout=12) as response:
                data = json.loads(response.read().decode('utf-8'))
                skins = data.get("skins", [])
                added_cat = 0
                for s in skins:
                    tex_url = s.get("url")
                    raw_name = s.get("name") or ""
                    clean_name = raw_name.strip()
                    
                    if not tex_url or tex_url in seen_urls:
                        continue
                    
                    # Si no tiene nombre o es inválido, nombrar con la categoría capitalizada
                    if not is_clean_name(clean_name):
                        clean_name = f"{cat.capitalize()} #{len(unique_skins) + 1}"
                    else:
                        # Limitar longitud a 20 chars
                        clean_name = clean_name[:20].strip()

                    variant = s.get("variant") or s.get("model") or ""
                    model = "alex" if variant == "slim" else "steve"

                    unique_skins.append({
                        "name": clean_name,
                        "textureUrl": tex_url.replace("http://", "https://"),
                        "model": model,
                        "category": cat
                    })
                    seen_urls.add(tex_url)
                    added_cat += 1
                    
                    if len(unique_skins) >= target_count:
                        break
                print(f"[{cat}] +{added_cat} skins (Total: {len(unique_skins)})")
        except Exception as e:
            print(f"Error buscando categoría {cat}: {e}")
        time.sleep(0.3)

    print(f"Total skins obtenidas: {len(unique_skins)}")
    with open("skins_precargadas.json", "w", encoding="utf-8") as f:
        json.dump(unique_skins, f, ensure_ascii=False, indent=2)
    print("Guardado exitosamente en skins_precargadas.json")

    with open("skins_precargadas.js", "w", encoding="utf-8") as f:
        f.write("window.SKINS_PRECARGADAS = " + json.dumps(unique_skins, ensure_ascii=False) + ";\n")
    print("Guardado exitosamente en skins_precargadas.js")

if __name__ == "__main__":
    fetch_skins()
