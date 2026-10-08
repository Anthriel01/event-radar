import json, shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVENTS_JS = ROOT / "events.js"
SAMPLE = ROOT / "events.sample.js"


def main():
    today = date.today().isoformat()
    if EVENTS_JS.exists() and not SAMPLE.exists():
        shutil.copyfile(EVENTS_JS, SAMPLE)
    seen, out = set(), []
    for f in sorted((ROOT / "data").glob("*.json")):
        for e in json.loads(f.read_text(encoding="utf-8")):
            link = e.get("link")
            if not link or link in seen:
                continue
            end = e.get("tarih_bitis") or e.get("tarih")
            if e.get("tur") == "etkinlik" and end and end < today:
                continue
            e.pop("ornek", None)
            seen.add(link)
            out.append(e)
    out.sort(key=lambda e: e.get("tarih") or "9999")
    js = ("window.EVENTS_META = " + json.dumps({"guncelleme": today}, ensure_ascii=False) + ";\n"
          "window.EVENTS = " + json.dumps(out, ensure_ascii=False, indent=2) + ";\n")
    EVENTS_JS.write_text(js, encoding="utf-8")
    print(f"{len(out)} kayit -> events.js")


if __name__ == "__main__":
    main()
