#!/usr/bin/env python3
"""
Header ve footer'ı tools/site_common.py'deki tek kaynaktan tüm sayfalara uygular.

Header veya footer'da bir değişiklik yaptığında (yeni nav linki, footer
sütunu, sözleşmeler listesi vb.) SADECE tools/site_common.py'yi düzenle,
sonra bunu çalıştır:

    python3 tools/build_pages.py

Script her HTML dosyasındaki <header class="site-header">…</header> ve
<footer class="site-footer">…</footer> bloklarını taze üretilmiş olanla
değiştirir; sayfanın geri kalanına (başlık, <main> içeriği, script
etiketleri) dokunmaz. Legal sayfalar (kullanım koşulları, gizlilik
politikası, aydınlatma metni) tools/build_legal.py tarafından zaten
site_common kullanılarak üretiliyor — bu script'i onlar üzerinde
çalıştırmak zararsızdır (idempotent), ek bir güvenlik ağı sağlar.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_common  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# dosya yolu (repo köküne göre) -> (page_id, dil)
PAGE_FILES = [
    ("index.html",                 "home",        "tr"),
    ("destek.html",                "destek",      "tr"),
    ("hesap-silme.html",           "hesap-silme", "tr"),
    ("iletisim.html",              "iletisim",    "tr"),
    ("kullanim-kosullari.html",    "kosullar",    "tr"),
    ("gizlilik-politikasi.html",   "gizlilik",    "tr"),
    ("aydinlatma-metni.html",      "aydinlatma",  "tr"),
    ("cerez-politikasi.html",      "cerez",       "tr"),
    ("404.html",                   "404",         "tr"),
    ("en/index.html",              "home",        "en"),
    ("en/support.html",            "destek",      "en"),
    ("en/delete-account.html",     "hesap-silme", "en"),
    ("en/contact.html",            "iletisim",    "en"),
    ("en/terms.html",              "kosullar",    "en"),
    ("en/privacy-policy.html",     "gizlilik",    "en"),
    ("en/privacy-notice.html",     "aydinlatma",  "en"),
    ("en/cookie-policy.html",      "cerez",       "en"),
]


def replace_block(html, start_marker, end_marker, new_block, label, filename):
    start = html.find(start_marker)
    if start == -1:
        sys.exit("%s: %s bulunamadı" % (filename, label))
    end = html.find(end_marker, start)
    if end == -1:
        sys.exit("%s: %s kapanışı bulunamadı" % (filename, label))
    end += len(end_marker)
    return html[:start] + new_block + html[end:]


def main():
    changed, unchanged = 0, 0
    for rel_path, page_id, lang in PAGE_FILES:
        path = os.path.join(ROOT, rel_path)
        if not os.path.exists(path):
            sys.exit("Bulunamadı: %s" % rel_path)

        with open(path, encoding="utf-8") as fh:
            original = fh.read()

        updated = replace_block(
            original, '<header class="site-header">', "</header>",
            site_common.render_header(page_id, lang), "header", rel_path,
        )
        updated = replace_block(
            updated, '<footer class="site-footer">', "</footer>",
            site_common.render_footer(page_id, lang), "footer", rel_path,
        )

        if updated != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(updated)
            print("güncellendi: %s" % rel_path)
            changed += 1
        else:
            unchanged += 1

    print("\n%d dosya güncellendi, %d dosya zaten günceldi." % (changed, unchanged))


if __name__ == "__main__":
    main()
