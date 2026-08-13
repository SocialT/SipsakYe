#!/usr/bin/env python3
"""
Doldurulmamış alanları bulur. Site yayına alınmadan önce çıktı boş olmalı.

Kullanım:  python3 tools/check_placeholders.py
Çıkış kodu: doldurulmamış alan varsa 1, temizse 0.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PH_RE = re.compile(r'<span class="ph">(.*?)</span>', re.S)


def main():
    findings = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "tools", "deploy")]
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            path = os.path.join(base, name)
            rel = os.path.relpath(path, ROOT)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for i, line in enumerate(text.splitlines(), 1):
                for m in PH_RE.finditer(line):
                    label = re.sub(r"\s+", " ", m.group(1)).strip()
                    findings.append((rel, i, label))

    if not findings:
        print("✓ Doldurulmamış alan yok — site yayına hazır.")
        return 0

    print("Doldurulması gereken %d alan var:\n" % len(findings))
    current = None
    for rel, line, label in findings:
        if rel != current:
            print("  %s" % rel)
            current = rel
        print("    satır %-4d %s" % (line, label))
    print(
        "\nBu alanlar 6563 sayılı E-Ticaret Kanunu gereği zorunludur ve\n"
        "App Store / Google Play inceleme ekipleri tarafından kontrol edilir."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
