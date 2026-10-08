import json, re, subprocess, sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / ".cache" / "conference-data"
OUT = ROOT / "data" / "confs.json"
URL = "https://github.com/tech-conferences/conference-data.git"
AI_TOPICS = {"data", "general", "opensource", "python"}
AI_RE = re.compile(r"(?<![A-Za-z0-9])(AI|ML|LLM|GenAI|machine\s+learning|artificial\s+intelligence)(?![A-Za-z0-9])", re.I)


def sync():
    if (REPO / ".git").exists():
        subprocess.run(["git", "-C", str(REPO), "pull", "--quiet"], check=True)
    else:
        REPO.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", "--quiet", URL, str(REPO)], check=True)


def main():
    sync()
    today = date.today()
    limit = today + timedelta(days=90)
    seen, out = set(), []
    for year in (today.year, today.year + 1):
        for f in sorted((REPO / "conferences" / str(year)).glob("*.json")):
            topic = f.stem
            if topic == "security":
                kat = "siber"
            elif topic in AI_TOPICS:
                kat = "yapay-zeka"
            else:
                continue
            for c in json.loads(f.read_text(encoding="utf-8")):
                url = c.get("url")
                try:
                    start = date.fromisoformat(c["startDate"])
                except (KeyError, ValueError, TypeError):
                    continue
                if not url or url in seen or not today <= start <= limit:
                    continue
                name = c.get("name") or ""
                if kat == "yapay-zeka" and not (AI_RE.search(name) or AI_RE.search(url)):
                    continue
                seen.add(url)
                country = c.get("country")
                yer = ", ".join(x for x in (c.get("city"), country) if x) or None
                out.append({
                    "tur": "etkinlik", "ad": name, "tarih": c["startDate"],
                    "tarih_bitis": c.get("endDate"), "yer": yer, "aciklama": None,
                    "link": url, "kaynak": "confs.tech",
                    "bolge": "turkiye" if (country or "").lower() in ("türkiye", "turkiye", "turkey") else "global",
                    "ucret": "bilinmiyor", "sertifika": "bilinmiyor", "format": "bilinmiyor",
                    "kategori": kat, "dogrulanmadi": False,
                })
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(out)} kayit -> {OUT.name}")


if __name__ == "__main__":
    sys.exit(main())
