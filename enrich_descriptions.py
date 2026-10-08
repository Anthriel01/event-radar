import html, json, re, sys, time, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
CONFS = ROOT / "data" / "confs.json"
CACHE = ROOT / ".cache" / "descriptions.json"
UA = "Mozilla/5.0 (compatible; EtkinlikRadari/1.0)"
MAX_BYTES = 500 * 1024
MAX_LEN = 220
BAD_RE = re.compile(r"cookie|çerez|javascript|enable js|browser", re.I)


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.og = self.meta = None

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        a = {k.lower(): v for k, v in attrs if v is not None}
        content = a.get("content")
        if not content:
            return
        if a.get("property", "").lower() == "og:description" and self.og is None:
            self.og = content
        elif a.get("name", "").lower() == "description" and self.meta is None:
            self.meta = content


def clean(text):
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    if len(text) < 40 or BAD_RE.search(text):
        return None
    if len(text) > MAX_LEN:
        text = text[:MAX_LEN].rsplit(" ", 1)[0].rstrip(" ,.;:-") + "…"
    return text


def fetch(link):
    """Returns description or None; raises on network/HTTP error."""
    if urlparse(link).scheme not in ("http", "https"):
        return None
    req = urllib.request.Request(link, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read(MAX_BYTES)
        charset = r.headers.get_content_charset() or "utf-8"
    p = MetaParser()
    p.feed(raw.decode(charset, errors="replace"))
    for cand in (p.og, p.meta):
        if cand and (d := clean(cand)):
            return d
    return None


def main():
    recs = json.loads(CONFS.read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    todo = [r["link"] for r in recs if r.get("link") and r["link"] not in cache]
    todo = list(dict.fromkeys(todo))
    print(f"{len(todo)} yeni link cekilecek", file=sys.stderr)
    for i, link in enumerate(todo):
        if i:
            time.sleep(1)
        try:
            cache[link] = fetch(link)
        except Exception as e:
            print(f"hata {link}: {e}", file=sys.stderr)
            continue
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    found = 0
    for r in recs:
        r["aciklama"] = cache.get(r.get("link"))
        found += r["aciklama"] is not None
    CONFS.write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"aciklama bulundu: {found}, null: {len(recs) - found}")


if __name__ == "__main__":
    main()
