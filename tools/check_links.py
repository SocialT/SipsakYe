#!/usr/bin/env python3
"""
Site içi bağlantıları ve çapa (#id) hedeflerini doğrular.
Kırık bağlantı, App Store incelemesinde doğrudan ret sebebidir.

Kullanım:  python3 tools/check_links.py
Çıkış kodu: kırık bağlantı varsa 1, temizse 0.
"""

import os
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "tools", "deploy"}

HREF_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(files):
            if name.endswith(".html"):
                yield os.path.join(base, name)


def main():
    ids = {}
    for path in html_files():
        with open(path, encoding="utf-8") as fh:
            ids[os.path.relpath(path, ROOT)] = set(ID_RE.findall(fh.read()))

    problems = []
    for path in html_files():
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        for raw in HREF_RE.findall(text):
            if raw.startswith(("mailto:", "tel:", "data:", "https://", "http://", "//")):
                continue

            parsed = urlparse(raw)
            target_path, anchor = unquote(parsed.path), parsed.fragment

            if not target_path:                      # aynı sayfada çapa
                target_rel = rel
            elif target_path.startswith("/"):        # kök göreli
                candidate = target_path.lstrip("/")
                if candidate == "" or candidate.endswith("/"):
                    candidate += "index.html"
                target_rel = candidate
            else:                                    # dosya göreli
                target_rel = os.path.normpath(
                    os.path.join(os.path.dirname(rel), target_path)
                )

            abs_target = os.path.join(ROOT, target_rel)
            if not os.path.exists(abs_target):
                problems.append((rel, raw, "dosya yok: %s" % target_rel))
                continue

            if anchor and target_rel.endswith(".html"):
                if anchor not in ids.get(target_rel, set()):
                    problems.append((rel, raw, "çapa yok: #%s" % anchor))

    if not problems:
        print("✓ Tüm iç bağlantılar ve çapalar geçerli.")
        return 0

    print("%d kırık bağlantı bulundu:\n" % len(problems))
    current = None
    for rel, raw, why in problems:
        if rel != current:
            print("  %s" % rel)
            current = rel
        print("    %-52s %s" % (raw, why))
    return 1


if __name__ == "__main__":
    sys.exit(main())
