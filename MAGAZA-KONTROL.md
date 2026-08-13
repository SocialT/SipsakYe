# Mağazaya vermeden önce kontrol listesi

App Store ve Google Play incelemesinde en sık karşılaşılan ret sebeplerine göre
hazırlandı. Site tarafındaki maddeler bu depoda karşılanıyor; uygulama
tarafındakiler sizde.

---

## 1. Site yayında ve erişilebilir

- [ ] `https://sipsakye.com` HTTPS üzerinden açılıyor, sertifika geçerli
- [ ] `www.sipsakye.com` kök alan adına yönleniyor
- [ ] Cloudflare SSL modu **Full (strict)** (Flexible **değil**)
- [ ] `python3 tools/check_links.py` temiz — kırık iç bağlantı yok
- [ ] `python3 tools/check_placeholders.py` temiz — künye alanları dolu
- [ ] Var olmayan bir adres denendiğinde 404 sayfası çıkıyor (`/olmayan-sayfa`)
- [ ] Sayfalar telefondan açıldığında düzgün görünüyor — reviewer telefondan bakabiliyor
- [ ] Hukuki sayfalar giriş yapmadan, doğrudan URL ile açılıyor

## 2. App Store Connect alanları

| Alan | Değer |
|------|-------|
| Support URL | `https://sipsakye.com/destek.html` |
| Privacy Policy URL | `https://sipsakye.com/gizlilik-politikasi.html` |
| Marketing URL (opsiyonel) | `https://sipsakye.com/` |
| EULA | Kendi metniniz: `https://sipsakye.com/kullanim-kosullari.html` |

- [ ] Bu URL'lerin hepsi tarayıcıda açılıyor, hiçbiri 404 vermiyor
- [ ] **App Privacy** beyanı, gizlilik politikasındaki veri kategorileriyle
      birebir aynı (konum, iletişim, finansal, kullanıcı içeriği, tanımlayıcılar)
- [ ] Uygulama açıklamasında Android/Google Play'den bahsedilmiyor
- [ ] Ekran görüntüleri uygulamanın gerçek halini gösteriyor

## 3. Google Play Console alanları

| Alan | Değer |
|------|-------|
| Gizlilik politikası URL | `https://sipsakye.com/gizlilik-politikasi.html` |
| Hesap silme URL | `https://sipsakye.com/hesap-silme.html` |
| Destek e-postası | `sipsakye0@gmail.com` |
| Web sitesi | `https://sipsakye.com/` |

- [ ] **Data safety** formu dolduruldu ve gizlilik politikasıyla çelişmiyor
- [ ] Hesap silme URL'si *Data safety → Data deletion* bölümüne girildi
- [ ] Konum izni kullanılıyorsa gerekçe beyanı yapıldı
- [ ] İçerik derecelendirme anketi dolduruldu

## 4. Uygulama tarafı — mağaza zorunlulukları

- [ ] **Uygulama içinde hesap silme var** (Apple 5.1.1(v)).
      `hesap-silme.html` sayfasındaki adımlar *Hesabım → Ayarlar → Hesabımı sil*
      diyor — uygulamadaki gerçek akış farklıysa **sayfayı güncelleyin**
- [ ] Yorum/puan için **kötüye kullanım bildirme** mekanizması var (Apple 1.2)
- [ ] Uygunsuz içerik filtreleme ve kullanıcı engelleme mevcut (Apple 1.2)
- [ ] Anlık bildirim uygulamanın çalışması için **zorunlu değil** (Apple 4.5.4)
- [ ] Pazarlama amaçlı bildirim için ayrı izin alınıyor (Apple 4.5.4 + İYS)
- [ ] Konum izni istenirken gerekçe açıkça gösteriliyor
- [ ] İnceleme ekibi için **test hesabı** hazırlandı ve App Review Notes'a yazıldı
      (giriş OTP ile yapılıyorsa bunu mutlaka nota ekleyin — reviewer SMS
      alamazsa uygulamayı reddeder)
- [ ] Uygulamanın hizmet verdiği bölge dışından bakan reviewer boş ekran
      görmüyor; en azından örnek içerik veya açıklama gösteriliyor

## 5. Mağaza rozetleri

Uygulama yayına girene kadar rozetler "Yakında" durumunda ve tıklanamaz —
böylece kırık link oluşmuyor.

Yayına girdikten sonra `index.html` ve `en/index.html` içinde:

- [ ] `store-badge--soon` sınıfı kaldırılıp `<span>` etiketleri `<a href="…">`
      yapıldı, gerçek mağaza bağlantıları eklendi
- [ ] "Yakında / Coming soon" yazıları "App Store'dan indir" / "Download on the"
      şeklinde güncellendi
- [ ] Hero altındaki "Uygulama yayına hazırlanıyor" notu ve CTA bölümündeki
      "çok yakında yayında" metni güncellendi
- [ ] Resmî rozet görselleri kullanıldı
      ([Apple](https://developer.apple.com/app-store/marketing/guidelines/),
      [Google](https://play.google.com/intl/en_us/badges/)) — şu an kullanılan
      rozetler kendi çizimimiz; marka kılavuzları resmî varlıkların
      kullanılmasını ister

## 6. Yasal

- [ ] `HUKUKI-EKSIKLER.md` dosyasındaki A grubu maddeler giderildi
- [ ] Künye bilgileri girildi (`iletisim.html`, `en/contact.html`)
- [ ] ETBİS kaydı yapıldı, numarası künyeye eklendi
- [ ] Pazarlama bildirimi gönderilecekse İYS kaydı tamamlandı
- [ ] Gizlilik politikasındaki üçüncü taraf servis listesi uygulamadaki
      gerçek SDK'larla eşleşiyor

## 7. Yayın sonrası

- [ ] `sitemap.xml` Google Search Console'a gönderildi
- [ ] Destek e-postası düzenli kontrol ediliyor — reviewer yazabiliyor,
      dönüş alamazsa reddedebiliyor
- [ ] Hukuki metinler güncellendiğinde `python3 tools/build_legal.py` yeniden
      çalıştırılıp değişiklik push edildi
