#!/usr/bin/env python3
"""
Header ve footer için TEK kaynak.

Bu dosya header/footer'ın gerçek HTML'ini üretir. Header veya footer'da bir
şey değiştirmek istediğinde SADECE burayı düzenle, sonra:

    python3 tools/build_pages.py

çalıştır — script bunu her sayfaya otomatik uygular. Sayfa gövdelerine
(hero, SSS, kart içerikleri vb.) bu dosya dokunmaz; yalnızca her HTML
dosyasındaki <header class="site-header">…</header> ve
<footer class="site-footer">…</footer> bloklarını değiştirir.
"""

# --------------------------------------------------------------------------
# Sayfa kayıt defteri: her sayfanın TR/EN karşılığı ve URL'leri.
# Yeni bir sayfa eklediğinde buraya bir satır ekle, build_pages.py'deki
# PAGE_FILES listesine de dosya yolunu ekle — bu kadar.
# --------------------------------------------------------------------------
PAGES = {
    "home":        {"url_tr": "/",                        "url_en": "/en/"},
    "destek":      {"url_tr": "/destek.html",              "url_en": "/en/support.html"},
    "hesap-silme": {"url_tr": "/hesap-silme.html",         "url_en": "/en/delete-account.html"},
    "iletisim":    {"url_tr": "/iletisim.html",            "url_en": "/en/contact.html"},
    "kosullar":    {"url_tr": "/kullanim-kosullari.html",  "url_en": "/en/terms.html"},
    "onbilgi":     {"url_tr": "/on-bilgilendirme-formu.html", "url_en": "/en/pre-contract-information.html"},
    "gizlilik":    {"url_tr": "/gizlilik-politikasi.html", "url_en": "/en/privacy-policy.html"},
    "aydinlatma":  {"url_tr": "/aydinlatma-metni.html",    "url_en": "/en/privacy-notice.html"},
    "cerez":       {"url_tr": "/cerez-politikasi.html",    "url_en": "/en/cookie-policy.html"},
    # 404 kendi diline özel değil; dil değiştirince ana sayfaya döner.
    "404":         {"url_tr": "/",                        "url_en": "/en/"},
}

# "Sözleşmeler / Legal" açılır menüsündeki dört belge — footer'daki
# "Yasal" sütunuyla birebir aynı liste, tek yerden besleniyor.
LEGAL_ITEMS = [
    # page_id,      TR etiket,              EN etiket
    ("kosullar",   "Kullanım Koşulları",     "Terms of Use"),
    ("onbilgi",    "Ön Bilgilendirme Formu", "Pre-Contract Information Form"),
    ("gizlilik",   "Gizlilik Politikası",    "Privacy Policy"),
    ("aydinlatma", "Aydınlatma Metni",       "Privacy Notice"),
    ("cerez",      "Çerez Politikası",       "Cookie Policy"),
]

BRAND_MARK_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z"/></svg>'
)
SUN_SVG = (
    '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round"><circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
)
MOON_SVG = (
    '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>'
)
BURGER_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
)


def render_header(page_id, lang):
    """page_id: PAGES sözlüğündeki anahtar. lang: 'tr' veya 'en'."""
    page = PAGES[page_id]
    is_tr = lang == "tr"
    home = page_id == "home"

    brand_href = "/" if is_tr else "/en/"
    aria_label = "Ana menü" if is_tr else "Main menu"
    theme_label = "Koyu / açık tema değiştir" if is_tr else "Toggle dark / light theme"
    menu_label = "Menüyü aç" if is_tr else "Open menu"

    if is_tr:
        sss_href = "#sss" if home else "/#sss"
        destek_current = ' aria-current="page"' if page_id == "destek" else ""
        hesap_current = ' aria-current="page"' if page_id == "hesap-silme" else ""
        iletisim_current = ' aria-current="page"' if page_id == "iletisim" else ""
        legal_label = "Sözleşmeler"
        nav_faq = f'<a class="nav__link" href="{sss_href}">SSS</a>'
        nav_support = f'<a class="nav__link" href="/destek.html"{destek_current}>Destek</a>'
        nav_hesap = f'<a class="nav__link" href="/hesap-silme.html"{hesap_current}>Hesap Sil</a>'
        nav_iletisim = f'<a class="nav__link" href="/iletisim.html"{iletisim_current}>İletişim</a>'
    else:
        faq_href = "#faq" if home else "/en/#faq"
        support_current = ' aria-current="page"' if page_id == "destek" else ""
        hesap_current = ' aria-current="page"' if page_id == "hesap-silme" else ""
        iletisim_current = ' aria-current="page"' if page_id == "iletisim" else ""
        legal_label = "Legal"
        nav_faq = f'<a class="nav__link" href="{faq_href}">FAQ</a>'
        nav_support = f'<a class="nav__link" href="/en/support.html"{support_current}>Support</a>'
        nav_hesap = f'<a class="nav__link" href="/en/delete-account.html"{hesap_current}>Delete Account</a>'
        nav_iletisim = f'<a class="nav__link" href="/en/contact.html"{iletisim_current}>Contact</a>'

    panel_links = []
    for pid, label_tr, label_en in LEGAL_ITEMS:
        url = PAGES[pid]["url_tr"] if is_tr else PAGES[pid]["url_en"]
        label = label_tr if is_tr else label_en
        current = ' aria-current="page"' if pid == page_id else ""
        panel_links.append(f'          <a href="{url}"{current}>{label}</a>')
    panel_html = "\n".join(panel_links)
    is_legal_page = page_id in {pid for pid, _, _ in LEGAL_ITEMS}
    dropdown_class = "nav-dropdown is-active" if is_legal_page else "nav-dropdown"

    nav_legal = f'''<details class="{dropdown_class}">
        <summary>{legal_label}<span class="nav-dropdown__caret" aria-hidden="true"></span></summary>
        <div class="nav-dropdown__panel">
{panel_html}
        </div>
      </details>'''

    if is_tr:
        lang_switch = f'''<div class="lang-switch">
        <a href="{page['url_tr']}" aria-current="true" hreflang="tr">TR</a>
        <a href="{page['url_en']}" hreflang="en">EN</a>
      </div>'''
    else:
        lang_switch = f'''<div class="lang-switch">
        <a href="{page['url_tr']}" hreflang="tr">TR</a>
        <a href="{page['url_en']}" aria-current="true" hreflang="en">EN</a>
      </div>'''

    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{brand_href}">
      <span class="brand__mark" aria-hidden="true">
        {BRAND_MARK_SVG}
      </span>
      Şipşak Ye
    </a>
    <nav class="nav" id="nav" aria-label="{aria_label}">
      {nav_faq}
      {nav_support}
      {nav_hesap}
      {nav_iletisim}
      {nav_legal}
    </nav>
    <div class="header-tools">
      {lang_switch}
      <button class="icon-btn theme-toggle" type="button" aria-label="{theme_label}">
        {SUN_SVG}
        {MOON_SVG}
      </button>
      <button class="icon-btn nav-toggle" type="button" aria-label="{menu_label}" aria-expanded="false" aria-controls="nav">
        {BURGER_SVG}
      </button>
    </div>
  </div>
</header>'''


def render_footer(page_id, lang):
    page = PAGES[page_id]
    is_tr = lang == "tr"
    brand_href = "/" if is_tr else "/en/"

    if is_tr:
        about_p = "Yemek ve market siparişini tek uygulamada birleştiren online sipariş platformu."
        app_h4, app_items = "Uygulama", ['<li><a href="/#sss">Sık sorulan sorular</a></li>']
        support_h4 = "Destek"
        support_items = [
            '<li><a href="/destek.html">Destek merkezi</a></li>',
            '<li><a href="/hesap-silme.html">Hesap silme</a></li>',
            '<li><a href="/iletisim.html">İletişim ve künye</a></li>',
            '<li><a href="mailto:sipsakye0@gmail.com">sipsakye0@gmail.com</a></li>',
        ]
        legal_h4 = "Yasal"
        copyright_line = '&copy; <span data-year>2026</span> Şipşak Ye. Tüm hakları saklıdır.'
        switch_label = "English"
        switch_href = page["url_en"]
    else:
        about_p = "An online ordering platform that brings food and grocery delivery together in one app."
        app_h4, app_items = "App", ['<li><a href="/en/#faq">FAQ</a></li>']
        support_h4 = "Support"
        support_items = [
            '<li><a href="/en/support.html">Support centre</a></li>',
            '<li><a href="/en/delete-account.html">Delete account</a></li>',
            '<li><a href="/en/contact.html">Contact &amp; company details</a></li>',
            '<li><a href="mailto:sipsakye0@gmail.com">sipsakye0@gmail.com</a></li>',
        ]
        legal_h4 = "Legal"
        copyright_line = '&copy; <span data-year>2026</span> Şipşak Ye. All rights reserved.'
        switch_label = "Türkçe"
        switch_href = page["url_tr"]

    legal_items = []
    for pid, label_tr, label_en in LEGAL_ITEMS:
        url = PAGES[pid]["url_tr"] if is_tr else PAGES[pid]["url_en"]
        label = label_tr if is_tr else label_en
        legal_items.append(f'          <li><a href="{url}">{label}</a></li>')

    app_items_html = "\n".join("          " + i for i in app_items)
    support_items_html = "\n".join("          " + i for i in support_items)
    legal_items_html = "\n".join(legal_items)

    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="{brand_href}">
          <span class="brand__mark" aria-hidden="true">
            {BRAND_MARK_SVG}
          </span>
          Şipşak Ye
        </a>
        <p>{about_p}</p>
      </div>
      <div class="footer-col">
        <h4>{app_h4}</h4>
        <ul>
{app_items_html}
        </ul>
      </div>
      <div class="footer-col">
        <h4>{support_h4}</h4>
        <ul>
{support_items_html}
        </ul>
      </div>
      <div class="footer-col">
        <h4>{legal_h4}</h4>
        <ul>
{legal_items_html}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{copyright_line}</span>
      <span><a href="{switch_href}">{switch_label}</a></span>
    </div>
  </div>
</footer>'''
