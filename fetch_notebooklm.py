import html, json, re, subprocess, sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
OUT = ROOT / "data" / "tr.json"
RAW = CACHE / "nlm_raw.json"

ENUMS = {
    "bolge": ({"yakin", "turkiye", "global"}, "turkiye"),
    "ucret": ({"ucretli", "ucretsiz", "bilinmiyor"}, "bilinmiyor"),
    "sertifika": ({"var", "yok", "bilinmiyor"}, "bilinmiyor"),
    "format": ({"online", "yuzyuze", "hibrit", "bilinmiyor"}, "bilinmiyor"),
    "kategori": ({"siber", "yapay-zeka", "diger"}, "diger"),
}
FIELDS = ["tur", "ad", "tarih", "tarih_bitis", "yer", "aciklama", "link", "kaynak",
          "bolge", "ucret", "sertifika", "format", "kategori"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Fail(Exception):
    pass


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or ""), (p.stderr or "")


def prepare_query(today):
    q = (ROOT / "sorgu.txt").read_text(encoding="utf-8")
    q = q.replace("{BUGUN}", today.isoformat()).replace("{BITIS}", (today + timedelta(days=90)).isoformat())
    CACHE.mkdir(exist_ok=True)
    f = CACHE / "sorgu_hazir.txt"
    f.write_text(q, encoding="utf-8")
    return f


def extract_array(text):
    """Ham çıktıdan JSON dizisini ayıkla (answer sarmalı / ```json çiti destekli)."""
    def unwrap(obj, depth=0):
        if isinstance(obj, list):
            return obj
        if depth > 3:
            return None
        if isinstance(obj, dict):
            for k in ("answer", "text", "response"):
                if k in obj:
                    r = unwrap(obj[k], depth + 1)
                    if r is not None:
                        return r
        if isinstance(obj, str):
            s = obj.strip()
            m = re.search(r"```(?:json)?\s*(.*?)```", s, re.S)
            if m:
                s = m.group(1).strip()
            try:
                return unwrap(json.loads(s), depth + 1)
            except ValueError:
                i, j = s.find("["), s.rfind("]")
                if i != -1 and j > i:
                    try:
                        return unwrap(json.loads(s[i:j + 1]), depth + 1)
                    except ValueError:
                        return None
        return None

    return unwrap(text)


def clean(v):
    if isinstance(v, str):
        return html.unescape(v).replace("\\_", "_")
    return v


def host(url):
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def source_hosts():
    code, out, err = run(["notebooklm", "source", "list", "--json"])
    if code != 0:
        return None
    try:
        data = json.loads(out)
    except ValueError:
        return None
    hosts = {host(s["url"]) for s in data.get("sources", []) if s.get("url")}
    return hosts or None


def suspicious(e):
    p = urlparse(e["link"])
    path = p.path.strip("/")
    return path == "" or path.lower() in ("en", "tr")


def main():
    today = date.today()
    qfile = prepare_query(today)
    code, out, err = run(["notebooklm", "ask", "--prompt-file", str(qfile), "--json"])
    if code != 0:
        raise Fail(f"notebooklm ask basarisiz (kod {code}): {(err or out).strip()[:500]}")
    arr = extract_array(out)
    if arr is None:
        RAW.write_text(out, encoding="utf-8")
        raise Fail(f"Cikti ayiklanamadi, ham cikti {RAW} dosyasina yazildi")
    if not arr:
        raise Fail("Bos cikti")

    hosts = source_hosts()
    if hosts is None:
        print("UYARI: kaynak host'lari alinamadi; dogrulanmadi=false birakildi.")

    dropped, out_list, seen = Counter(), [], set()
    today_s = today.isoformat()
    for raw in arr:
        if not isinstance(raw, dict):
            dropped["kayit degil"] += 1
            continue
        e = {clean(k): clean(v) for k, v in raw.items()}
        e = {k: e.get(k) for k in FIELDS}
        if e["tur"] not in ("etkinlik", "egitim"):
            dropped["bilinmeyen tur"] += 1
            continue
        link = e["link"]
        if not isinstance(link, str) or urlparse(link).scheme not in ("http", "https") or not urlparse(link).netloc:
            dropped["gecersiz link"] += 1
            continue
        for k in ("tarih", "tarih_bitis"):
            if not (isinstance(e[k], str) and DATE_RE.match(e[k])):
                e[k] = None
        end = e["tarih_bitis"] or e["tarih"]
        if e["tur"] == "etkinlik" and end and end < today_s:
            dropped["gecmis etkinlik"] += 1
            continue
        if link in seen:
            dropped["tekrar link"] += 1
            continue
        for k, (allowed, default) in ENUMS.items():
            if e[k] not in allowed:
                e[k] = default
        seen.add(link)
        e["dogrulanmadi"] = bool(hosts) and host(link) not in hosts
        out_list.append(e)

    if not out_list:
        raise Fail("Gecerli kayit kalmadi")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out_list, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(arr)} kayit geldi, {len(out_list)} yazildi -> {OUT.relative_to(ROOT)}")
    if dropped:
        print("Atilanlar:", ", ".join(f"{k}: {v}" for k, v in dropped.items()))
    print("Bolge:", dict(Counter(e["bolge"] for e in out_list)))
    print("Kategori:", dict(Counter(e["kategori"] for e in out_list)))
    print("Dogrulanmadi=true:", sum(e["dogrulanmadi"] for e in out_list))
    sus = [e for e in out_list if suspicious(e)]
    if sus:
        print("Supheli link (genel/ana sayfa):")
        for e in sus:
            print(f"  - {e['ad']} -> {e['link']}")


if __name__ == "__main__":
    try:
        main()
    except Fail as ex:
        print(f"HATA: {ex}. Mevcut data/tr.json korundu.", file=sys.stderr)
        sys.exit(1)
