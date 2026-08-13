#!/usr/bin/env python3
"""
Word belgelerinden hukuki sayfaları üretir.

Metinlere içerik olarak dokunulmaz; yalnızca aşağıdaki TYPO_FIXES listesindeki
açık yazım hataları düzeltilir ve her düzeltme çalıştırma sırasında raporlanır.

Kullanım:  python3 tools/build_legal.py
"""

import html
import json
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# --------------------------------------------------------------------------
# Yalnızca tartışmasız yazım/boşluk hataları. Anlamı değiştiren hiçbir
# düzeltme buraya eklenmemeli — hukuki metnin içeriği olduğu gibi kalır.
# --------------------------------------------------------------------------
TYPO_FIXES = [
    ("işllenmemekedir", "işlenmemektedir"),
    ("sahptirler", "sahiptirler"),
    ("YŞipşak Ye", "Şipşak Ye"),
    ("Şipşak Ye Platformuun", "Şipşak Ye Platformunun"),
    ("Kanun'unilgili", "Kanun'un ilgili"),
    ("Kanun’unilgili", "Kanun’un ilgili"),
    ("platfromun", "platformun"),
    ("yükümlüğüğünün", "yükümlülüğünün"),
    ("edlimesi", "edilmesi"),
    ("Dondırma", "Dondurma"),
    ("dayalu", "dayalı"),
    ("tarımm", "tarım"),
    ("aralığığı", "aralığı"),
    ("sürelieri", "süreleri"),
    ("unutulmamamalı", "unutulmamalı"),
    ("yetklili", "yetkili"),
    ("kullanıcınınŞipşak", "kullanıcının Şipşak"),
    ("çözümündeAntalya", "çözümünde Antalya"),
    ("kapsamındaŞipşak", "kapsamında Şipşak"),
    ("işletmelerdende", "işletmelerinden de"),
    ("verileride", "verileri de"),
    ("alışkanlıklarıda", "alışkanlıkları da"),
    ("gümüş,bronz,altın", "gümüş, bronz, altın"),
    ("Sipsakye0@gmail.com", "sipsakye0@gmail.com"),
    ("sipsakye0@gmail.com a ,", "sipsakye0@gmail.com adresine,"),
    ("içerisinde,,", "içerisinde,"),
    ("nihaen", "nihayeten"),
    ("dosyalardanŞipşak", "dosyalardan Şipşak"),
]

EMAIL_RE = re.compile(r"\b(sipsakye0@gmail\.com)\b")
URL_RE = re.compile(r"\b(www\.sipsakye\.com)\b")

# Üst düzey başlık: "1. ", "III. ", "VIII. "
H2_RE = re.compile(r"^(?:[0-9]{1,2}|[IVX]{1,5})\.\s*\S")
# Alt başlık: "II.I. ", "V.III. "
H3_RE = re.compile(r"^[IVX]{1,5}\.[IVX]{1,5}\.\s*\S")


def paragraphs(docx_path):
    """docx -> [{t, list, ilvl, bold}]"""
    def text_of(node):
        out = []
        for n in node.iter():
            if n.tag == W + "t":
                out.append(n.text or "")
            elif n.tag == W + "tab":
                out.append(" ")
            elif n.tag == W + "br":
                out.append("\n")
        return "".join(out)

    z = zipfile.ZipFile(docx_path)
    root = ET.fromstring(z.read("word/document.xml"))
    result = []
    for p in root.iter(W + "p"):
        t = text_of(p).replace("\xa0", " ").strip()
        t = re.sub(r"[ \t]{2,}", " ", t)
        if not t:
            continue
        pPr = p.find(W + "pPr")
        is_list = pPr is not None and pPr.find(W + "numPr") is not None
        ilvl = 0
        if is_list:
            il = pPr.find(W + "numPr").find(W + "ilvl")
            if il is not None:
                ilvl = int(il.get(W + "val"))
        runs = [r for r in p.findall(W + "r") if text_of(r).strip()]
        bold = bool(runs) and all(
            r.find(W + "rPr") is not None and r.find(W + "rPr").find(W + "b") is not None
            for r in runs
        )
        result.append({"t": t, "list": is_list, "ilvl": ilvl, "bold": bold})
    return result


SPACE_BEFORE_PUNCT = re.compile(r"\s+([,;.:])")


def apply_fixes(text, tally):
    for wrong, right in TYPO_FIXES:
        if wrong in text:
            tally[wrong] = tally.get(wrong, 0) + text.count(wrong)
            text = text.replace(wrong, right)
    # Noktalama öncesi fazla boşluk — tamamen tipografik, anlamı etkilemez.
    fixed = SPACE_BEFORE_PUNCT.sub(r"\1", text)
    if fixed != text:
        tally["<noktalama öncesi boşluk>"] = tally.get("<noktalama öncesi boşluk>", 0) + 1
        text = fixed
    return text


def inline(text):
    """Kaçış + e-posta/URL bağlantıları."""
    out = html.escape(text, quote=False)
    out = EMAIL_RE.sub(r'<a href="mailto:\1">\1</a>', out)
    out = URL_RE.sub(r'<a href="https://sipsakye.com/">\1</a>', out)
    return out


def slugify(text):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    s = text.translate(tr).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60] or "bolum"


def render_body(paras, tally):
    """Paragraf listesini prose HTML + içindekiler girdilerine çevirir."""
    parts, toc = [], []
    open_list = False
    seen = {}

    def close_list():
        nonlocal open_list
        if open_list:
            parts.append("</ul>")
            open_list = False

    for p in paras[1:]:  # ilk paragraf belge başlığı, sayfa başlığında kullanılır
        t = apply_fixes(p["t"], tally)

        if p["list"]:
            if not open_list:
                parts.append('<ul>')
                open_list = True
            parts.append("  <li>%s</li>" % inline(t))
            continue

        close_list()

        is_h3 = bool(H3_RE.match(t))
        is_h2 = (not is_h3) and bool(H2_RE.match(t)) and len(t) < 110
        # Numarasız ama tamamı kalın kısa satırlar da alt başlık sayılır
        if not is_h2 and not is_h3 and p["bold"] and len(t) < 110 and not t.endswith((".", ":", ";")):
            is_h3 = True

        if is_h2 or is_h3:
            base = slugify(t)
            seen[base] = seen.get(base, 0) + 1
            anchor = base if seen[base] == 1 else "%s-%d" % (base, seen[base])
            tag = "h2" if is_h2 else "h3"
            parts.append('<%s id="%s">%s</%s>' % (tag, anchor, inline(t), tag))
            if is_h2:
                toc.append((anchor, t))
            continue

        parts.append("<p>%s</p>" % inline(t))

    close_list()
    return "\n".join(parts), toc


PAGE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Şipşak Ye</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://sipsakye.com/{slug}.html">
<link rel="alternate" hreflang="tr" href="https://sipsakye.com/{slug}.html">
<link rel="alternate" hreflang="en" href="https://sipsakye.com/en/{en_slug}.html">
<meta name="theme-color" content="#FF4D2D" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14100E" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Şipşak Ye">
<meta property="og:title" content="{title} — Şipşak Ye">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://sipsakye.com/{slug}.html">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/head.js"></script>
</head>
<body>
<a class="skip-link" href="#main">İçeriğe geç</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">
      <span class="brand__mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg>
      </span>
      Şipşak Ye
    </a>
    <nav class="nav" id="nav" aria-label="Ana menü">
      <a class="nav__link" href="/#ozellikler">Özellikler</a>
      <a class="nav__link" href="/#nasil-calisir">Nasıl çalışır</a>
      <a class="nav__link" href="/#sss">SSS</a>
      <a class="nav__link" href="/destek.html">Destek</a>
    </nav>
    <div class="header-tools">
      <div class="lang-switch">
        <a href="/{slug}.html" aria-current="true" hreflang="tr">TR</a>
        <a href="/en/{en_slug}.html" hreflang="en">EN</a>
      </div>
      <button class="icon-btn theme-toggle" type="button" aria-label="Koyu / açık tema değiştir">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
      </button>
      <button class="icon-btn nav-toggle" type="button" aria-label="Menüyü aç" aria-expanded="false" aria-controls="nav">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
</header>

<main id="main">
  <div class="page-head">
    <div class="wrap">
      <p class="breadcrumb"><a href="/">Ana sayfa</a> &rsaquo; {title}</p>
      <h1>{title}</h1>
      <p>{desc}</p>
      <p class="meta">Son güncelleme: {updated} &middot; Yürürlükteki metin Türkçedir.</p>
    </div>
  </div>

  <div class="wrap">
    <div class="doc-layout">
      <aside class="doc-toc">
        <h2>İçindekiler</h2>
        <ul>
{toc}
        </ul>
      </aside>

      <article class="prose">
{body}
        <div class="callout">
          <p><strong>Sorularınız mı var?</strong> Bu metinle ilgili her türlü soru, talep ve başvurunuzu
          <a href="mailto:sipsakye0@gmail.com">sipsakye0@gmail.com</a> adresine iletebilirsiniz.
          Diğer belgeler: <a href="/kullanim-kosullari.html">Kullanım Koşulları</a>,
          <a href="/gizlilik-politikasi.html">Gizlilik Politikası</a>,
          <a href="/aydinlatma-metni.html">Aydınlatma Metni</a>,
          <a href="/cerez-politikasi.html">Çerez Politikası</a>.</p>
        </div>
      </article>
    </div>
  </div>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="/">
          <span class="brand__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg>
          </span>
          Şipşak Ye
        </a>
        <p>Yemek ve market siparişini tek uygulamada birleştiren online sipariş platformu.</p>
      </div>
      <div class="footer-col">
        <h4>Uygulama</h4>
        <ul>
          <li><a href="/#ozellikler">Özellikler</a></li>
          <li><a href="/#nasil-calisir">Nasıl çalışır</a></li>
          <li><a href="/#sss">Sık sorulan sorular</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Destek</h4>
        <ul>
          <li><a href="/destek.html">Destek merkezi</a></li>
          <li><a href="/hesap-silme.html">Hesap silme</a></li>
          <li><a href="/iletisim.html">İletişim ve künye</a></li>
          <li><a href="mailto:sipsakye0@gmail.com">sipsakye0@gmail.com</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Yasal</h4>
        <ul>
          <li><a href="/kullanim-kosullari.html">Kullanım Koşulları</a></li>
          <li><a href="/gizlilik-politikasi.html">Gizlilik Politikası</a></li>
          <li><a href="/aydinlatma-metni.html">Aydınlatma Metni</a></li>
          <li><a href="/cerez-politikasi.html">Çerez Politikası</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Şipşak Ye. Tüm hakları saklıdır.</span>
      <span><a href="/en/{en_slug}.html">English</a></span>
    </div>
  </div>
</footer>

<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

DOCS = [
    {
        "src": "eb8dbdc0-Ki_isel_Verilerin_Korunmas____lenmesi_ve_Gizlilik_Politikas_.docx",
        "slug": "gizlilik-politikasi",
        "en_slug": "privacy-policy",
        "title": "Kişisel Verilerin Korunması, İşlenmesi ve Gizlilik Politikası",
        "desc": "Şipşak Ye Platformu'nun 6698 sayılı KVKK kapsamında kişisel verileri hangi ilkelerle işlediğini, sakladığını, aktardığını ve koruduğunu açıklayan politika metni.",
    },
    {
        "src": "a27e0e03-ayd_nlatma_metni.docx",
        "slug": "aydinlatma-metni",
        "en_slug": "privacy-notice",
        "title": "KVKK Aydınlatma Metni",
        "desc": "6698 sayılı Kişisel Verilerin Korunması Kanunu uyarınca hangi kişisel verilerinizin, hangi amaçla ve hangi hukuki sebeple işlendiğine ilişkin aydınlatma metni.",
    },
    {
        "src": "d872113e-mesafeli_sat___s_zle_mesi_ve_kullan_m_ko_ullar_.docx",
        "slug": "kullanim-kosullari",
        "en_slug": "terms",
        "title": "Mesafeli Satış Sözleşmesi ve Kullanım Koşulları",
        "desc": "Şipşak Ye Platformu üzerinden verilen siparişlere, ödeme ve teslimat süreçlerine, iptal ve iade koşullarına ilişkin sözleşme ve kullanım koşulları.",
    },
]

UPDATED = "13 Ağustos 2026"


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SY_DOCX_DIR", "")
    if not src_dir or not os.path.isdir(src_dir):
        sys.exit(
            "Kaynak .docx klasörü bulunamadı.\n"
            "Kullanım: python3 tools/build_legal.py /kaynak/klasor"
        )

    tally = {}
    for doc in DOCS:
        path = os.path.join(src_dir, doc["src"])
        if not os.path.exists(path):
            sys.exit("Bulunamadı: %s" % path)

        paras = paragraphs(path)
        body, toc = render_body(paras, tally)

        toc_html = "\n".join(
            '          <li><a href="#%s">%s</a></li>' % (a, html.escape(t, quote=False))
            for a, t in toc
        )
        out = PAGE.format(
            title=html.escape(doc["title"], quote=True),
            desc=html.escape(doc["desc"], quote=True),
            slug=doc["slug"],
            en_slug=doc["en_slug"],
            updated=UPDATED,
            toc=toc_html,
            body="\n".join("        " + line for line in body.splitlines()),
        )
        dest = os.path.join(ROOT, doc["slug"] + ".html")
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(out)
        print("yazıldı: %-28s (%d bölüm, %d paragraf)" % (doc["slug"] + ".html", len(toc), len(paras)))

    print("\nUygulanan yazım düzeltmeleri:")
    print("  %-28s -> %-28s x%d" % ("<noktalama öncesi boşluk>", "kaldırıldı", tally.get("<noktalama öncesi boşluk>", 0)))
    for wrong, right in TYPO_FIXES:
        n = tally.get(wrong, 0)
        flag = "  " if n else "! "
        print("%s%-28s -> %-28s x%d" % (flag, wrong, right, n))
    unused = [w for w, _ in TYPO_FIXES if not tally.get(w)]
    if unused:
        print("\nEşleşmeyen (gözden geçir): %s" % ", ".join(unused))


if __name__ == "__main__":
    main()
