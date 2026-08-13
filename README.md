# Şipşak Ye — tanıtım sitesi

[sipsakye.com](https://sipsakye.com) için statik tanıtım ve yasal bilgi sitesi.
Yemek ve market siparişi mobil uygulamasının App Store / Google Play
incelemesinde istenen tüm sayfaları içerir.

**Derleme adımı yok, çalışma zamanı bağımlılığı yok.** Saf HTML + CSS + ~2 KB
vanilla JS. Nginx dosyaları doğrudan servis eder.

---

## Sayfalar

| Türkçe | English | Amaç |
|--------|---------|------|
| `index.html` | `en/index.html` | Ana sayfa — uygulama tanıtımı |
| `destek.html` | `en/support.html` | **Apple Support URL** · SSS, iletişim, içerik bildirimi |
| `hesap-silme.html` | `en/delete-account.html` | **Google Play hesap silme URL'si** (zorunlu) |
| `kullanim-kosullari.html` | `en/terms.html` | Mesafeli Satış Sözleşmesi ve Kullanım Koşulları |
| `gizlilik-politikasi.html` | `en/privacy-policy.html` | **Gizlilik politikası URL'si** (iki mağaza için de zorunlu) |
| `aydinlatma-metni.html` | `en/privacy-notice.html` | KVKK Aydınlatma Metni |
| `cerez-politikasi.html` | `en/cookie-policy.html` | Çerez politikası |
| `iletisim.html` | `en/contact.html` | Künye — 6563 sayılı Kanun gereği zorunlu |
| `404.html` | — | Kırık link Apple'da ret sebebi |

Türkçe sayfalar kökte, İngilizce sayfalar `/en/` altında. Diller `hreflang`
etiketleriyle bağlı; otomatik dil yönlendirmesi **yok** (arama motorlarını ve
inceleme ekibini karıştırdığı için) — başlıktaki TR/EN düğmesi kullanılır.

## Dizin yapısı

```
├── index.html, destek.html, …      Türkçe sayfalar
├── en/                             İngilizce sayfalar
├── assets/
│   ├── css/style.css               Tüm tasarım sistemi (tek dosya)
│   ├── js/main.js                  Tema, mobil menü, scroll animasyonu
│   └── img/                        Üretilen ikonlar ve OG görseli
├── deploy/
│   ├── nginx.conf                  Sunucu bloğu
│   ├── DEPLOY.md                   Kurulum adımları
│   └── update.sh                   Sunucuda güncelleme
├── tools/
│   ├── build_legal.py              Word belgelerinden hukuki sayfa üretir
│   ├── make_icons.py               Favicon, PWA ikonları, OG görseli
│   ├── check_links.py              Kırık iç bağlantı kontrolü
│   └── check_placeholders.py       Doldurulmamış künye alanı kontrolü
├── HUKUKI-EKSIKLER.md              Belgelerdeki eksiklerin listesi
└── MAGAZA-KONTROL.md               Yayın öncesi kontrol listesi
```

## Nasıl düzenlenir

**Normal sayfalar** (ana sayfa, destek, hesap silme, iletişim, çerez, 404)
doğrudan HTML olarak düzenlenir. Başlık ve alt bilgi her sayfada tekrar eder;
birinde değişiklik yaparsanız diğerlerine de uygulayın.

**Hukuki sayfalar** (kullanım koşulları, gizlilik politikası, aydınlatma metni)
Word belgelerinden üretilir — elle düzenlemeyin, üzerine yazılır:

```bash
python3 tools/build_legal.py /kaynak/docx/klasoru
```

Betik belgelerin içeriğine dokunmaz; yalnızca `TYPO_FIXES` listesindeki yazım
hatalarını düzeltir ve her düzeltmeyi rapor eder.

**İkonlar** değişirse:

```bash
python3 tools/make_icons.py
```

## Yerelde çalıştırma

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Yayına almadan önce

```bash
python3 tools/check_placeholders.py   # künye alanları dolu mu
python3 tools/check_links.py          # kırık bağlantı var mı
```

İkisi de temiz olmalı. Ardından [`MAGAZA-KONTROL.md`](MAGAZA-KONTROL.md)
listesini gözden geçirin.

## Yayına alma

Ubuntu VPS + Nginx + Cloudflare kurulumunun tamamı
[`deploy/DEPLOY.md`](deploy/DEPLOY.md) dosyasında.

Özet: depoyu `/var/www/sipsakye.com` altına klonlayın, `deploy/nginx.conf`
dosyasını etkinleştirin, Cloudflare'de **Full (strict)** SSL modunu seçin.
Güncelleme `git pull` ile — yeniden başlatma gerekmez.

## Bilinen açık işler

- [ ] Künye bilgileri doldurulacak (`iletisim.html`, `en/contact.html`)
- [ ] Uygulama yayına girince mağaza rozetleri gerçek bağlantılarla
      değiştirilecek — şu an tıklanamaz "Yakında" durumunda
- [ ] Telefon maketi yerine gerçek ekran görüntüleri konulabilir
- [ ] [`HUKUKI-EKSIKLER.md`](HUKUKI-EKSIKLER.md) dosyasındaki maddeler
      avukat onayından geçirilecek
