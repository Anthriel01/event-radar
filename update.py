import subprocess, sys
from datetime import date

import enrich_descriptions, fetch_confs, merge


def git(*args):
    p = subprocess.run(["git", *args], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(f"HATA: git {' '.join(args)}\n{p.stdout}{p.stderr}", file=sys.stderr)
        sys.exit(1)
    return p.stdout


def git_step():
    if not git("status", "--porcelain", "--", "events.js", "data/").strip():
        print("Degisiklik yok.")
        return
    git("add", "events.js", "data/")
    git("commit", "-m", f"Veri güncellendi: {date.today().isoformat()}")
    print(git("push", "origin", "main"))


if __name__ == "__main__":
    args = set(sys.argv[1:])
    fetch_confs.main()
    if "--no-nlm" not in args:
        import fetch_notebooklm
        try:
            fetch_notebooklm.main()
        except (fetch_notebooklm.Fail, Exception) as ex:
            print(f"UYARI: fetch_notebooklm basarisiz ({ex}); eski tr.json kullaniliyor.", file=sys.stderr)
    enrich_descriptions.main()
    merge.main()
    if "--no-git" not in args:
        git_step()
    sys.exit(0)
