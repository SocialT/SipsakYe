# Hukuki belgelerde tespit edilen eksikler

Bu liste, siteye eklenen üç Word belgesinin (Mesafeli Satış Sözleşmesi ve
Kullanım Koşulları, KVKK Aydınlatma Metni, Gizlilik Politikası) incelenmesi
sonucunda çıkarılmıştır.

> **Bu bir hukuki görüş değildir.** Belgeleri hazırlayan veya kontrol edecek
> avukatınıza götürebilmeniz için hazırlanmış bir kontrol listesidir.
> Belgelerin içeriğine dokunulmamış, siteye oldukları gibi alınmıştır;
> yalnızca yazım hataları düzeltilmiştir (bkz. `tools/build_legal.py`
> içindeki `TYPO_FIXES` listesi ve çalıştırma raporu).

---

## A. Yayına almadan mutlaka giderilmesi gerekenler

### A1. Künye bilgileri hiçbir belgede yok — **en kritik eksik**

Mesafeli Satış Sözleşmesi'nin "1. Taraflar" maddesinde yalnızca site ve
uygulama adı yazıyor. Satıcı/sağlayıcı tarafında **ticaret unvanı, ad-soyad,
açık adres, vergi dairesi ve vergi numarası, telefon** bilgilerinin hiçbiri yok.

- **Neden önemli:** 6563 sayılı E-Ticaret Kanunu ve Mesafeli Sözleşmeler
  Yönetmeliği bu bilgilerin hem sözleşmede hem de sitede bulunmasını zorunlu
  kılıyor. App Store ve Google Play inceleme ekipleri de bu bilgiyi arıyor.
- **Sitedeki durum:** `iletisim.html` ve `en/contact.html` sayfalarında künye
  tablosu hazır, alanlar doldurulmayı bekliyor.
  Kontrol: `python3 tools/check_placeholders.py`
- **Ayrıca:** ETBİS (Elektronik Ticaret Bilgi Sistemi) kaydı e-ticaret
  faaliyeti için zorunludur; kayıt numarası künyede yer almalıdır.

### A2. Cayma hakkı hiç düzenlenmemiş

Sözleşmede cayma hakkına, süresine, kullanım şekline veya istisnalarına dair
tek bir madde yok.

- Mesafeli Sözleşmeler Yönetmeliği cayma hakkının düzenlenmesini zorunlu tutar.
- Gıda, çabuk bozulan veya son kullanma tarihi geçebilecek ürünler için
  Yönetmelik m.15 istisnası uygulanabilir — **ancak bu istisnanın sözleşmede
  açıkça yazılması gerekir.** "Yazmayınca uygulanmaz" durumu doğar.

### A3. Ön Bilgilendirme Formu yok

Mesafeli sözleşmelerde, sözleşmeden ayrı olarak tüketiciye sunulması ve
onaylatılması gereken bir Ön Bilgilendirme Formu bulunmalıdır (satıcı bilgileri,
toplam fiyat, ödeme ve teslimat, cayma hakkı, şikâyet mercileri).
Belgeler arasında bu form yok.

### A4. Madde 11 atlanmış

Mesafeli Satış Sözleşmesi 10. maddeden doğrudan 12. maddeye geçiyor.
İçerik kaybı mı yoksa numaralandırma hatası mı olduğu kontrol edilmeli.

### A5. Gizlilik Politikası'nda VI.I bölümü atlanmış

Politika `V.III`'ten doğrudan `VI.II. KİŞİSEL VERİ KATEGORİZASYONU` başlığına
geçiyor. `VI` ve `VI.I` bölümleri yok.

---

## B. Tüketici mevzuatı açısından riskli görülen hükümler

Bu maddeler, Tüketici Kanunu kapsamında **haksız şart** sayılıp tüketici hakem
heyeti veya mahkeme tarafından geçersiz kabul edilebilir.

### B1. "Stok bitiminde bilgi verme zorunluluğu yoktur"

> "Stok bitiminden kaynaklı sipariş teslimatının yapılamayacağı durumlarda
> müşteriye bilgi verilme zorunluluğu yoktur ve müşteri bundan dolayı bir hak
> talep edemez."

Sözleşmede **iki kez** geçiyor (9. ve 10. maddeler). Ödemesi alınmış bir
siparişin teslim edilememesi halinde tüketicinin bilgilendirilme ve iade hakkı
mevzuattan doğar; sözleşmeyle kaldırılamaz.

### B2. "Ücret iadesi yapıp yapmama hakkını saklı tutar"

> "Yemek siparişlerinde siparişleriniz hazırlanma aşamasına geçmiş ise ve
> ödemeyi herhangi bir yolla peşinen yapmışsanız […] platform yada işyerleri
> ücret iadesi yapıp yapmama hakkını saklı tutar."

İade yapılıp yapılmayacağını tamamen tek tarafın takdirine bırakan hüküm,
tüketici aleyhine dengesizlik oluşturduğu gerekçesiyle geçersiz sayılabilir.

### B3. Yetkili mahkeme maddesi

> "Sözleşme'nin ifasından doğabilecek her türlü uyuşmazlığın çözümünde
> Antalya Mahkemeleri ve İcra Müdürlükleri […] yetkilidir."

Tüketici işlemlerinde tüketicinin kendi yerleşim yerindeki tüketici hakem heyeti
ve tüketici mahkemesi de yetkilidir; bu madde tüketiciye karşı ileri sürülemez.
Sitede `iletisim.html` sayfasında bu durum ayrıca açıklanmıştır.

### B4. Fikri mülkiyet maddesinde kullanıcı içeriği devri

12. madde, kullanıcının yüklediği tüm içeriğe ilişkin FSEK kapsamındaki
**tüm mali hakların** platforma ait olduğunu düzenliyor. Bu kadar geniş bir
devir hükmü, kapsamının daraltılması açısından gözden geçirilmeli.

---

## C. KVKK ve mağaza uyumu açısından tamamlanması gerekenler

### C1. Ticari elektronik ileti (İYS) onay metni yok

Uygulamada pazarlama amaçlı **anlık bildirim** gönderiliyor. 6563 sayılı Kanun
ve İleti Yönetim Sistemi (İYS) mevzuatı uyarınca:

- Ticari elektronik ileti için **ayrı ve açık bir onay** alınmalı,
- Onaylar **İYS'ye kaydedilmeli**,
- Her iletide **ret hakkı (opt-out)** sunulmalıdır.

Sözleşmenin 3. maddesinde "kullanıcı tercihini belirleyebilir" ifadesi var ve
sipariş bildirimlerinin ticari ileti sayılmadığı belirtilmiş; ancak ayrı bir
açık rıza metni belgeler arasında yok.

### C2. Yurt dışı veri aktarımı eksik beyan edilmiş

Belgeler yurt dışı aktarımı yalnızca "iştirakler, hissedarlar ve iş ortakları"
üzerinden anlatıyor. Uygulamada anlık bildirim kullanıldığına göre büyük
olasılıkla **Firebase Cloud Messaging** veya benzeri bir servis devrede;
bu, Google'a yurt dışı veri aktarımı anlamına gelir.

- Kullanılan tüm üçüncü taraf servisleri (push, analitik, çökme raporlama,
  ödeme sağlayıcı) gizlilik politikasında **isim isim** sayılmalı.
- **Aynı liste Play Console "Data Safety" formu ve App Store Connect
  "App Privacy" beyanıyla birebir örtüşmeli.** Bu iki beyan arasındaki
  tutarsızlık, mağaza reddinin en sık sebebidir.

### C3. Hesap silme prosedürü sözleşmede net değil

Sözleşmenin 17. maddesi yalnızca "taraflar diledikleri zaman sona
erdirebilecektir" diyor. 5. maddede üyeliği sonlandırma talebine değiniliyor
ancak somut adımlar yok.

- **Google Play**, hesap oluşturan uygulamalar için uygulamayı yüklemeden
  erişilebilen bir hesap silme talebi URL'si zorunlu kılar.
  → Sitede `hesap-silme.html` / `en/delete-account.html` sayfaları bu amaçla
  hazırlandı; URL Play Console'a ayrıca girilmelidir.
- **Apple**, 5.1.1(v) gereği hesap silmenin **uygulama içinden** yapılabilmesini
  ister. Yalnızca web sayfası yeterli değildir.
  → Sitedeki sayfa, uygulama içi akışı *Hesabım → Ayarlar → Hesabımı sil*
  olarak tarif ediyor. **Uygulamadaki gerçek akış farklıysa sayfa
  güncellenmelidir** — tarif edilen adımın uygulamada bulunmaması ret sebebidir.

### C4. Çerez politikası belgeler arasında yoktu

Site için `cerez-politikasi.html` / `en/cookie-policy.html` sayfaları yazıldı.
İçerik sitenin gerçek durumunu yansıtıyor: **hiç çerez kullanılmıyor**, yalnızca
tema tercihi için yerel depolama (`sy-theme`). Siteye ileride analitik eklenirse
bu sayfa güncellenmelidir.

### C5. Kullanıcı içeriği ve şikâyet mekanizması

Uygulamada yorum, puan ve kullanıcı fotoğrafı var. Apple Guideline 1.2, kullanıcı
içeriği barındıran uygulamalarda içerik filtreleme, **kötüye kullanım bildirme
mekanizması**, kullanıcı engelleme ve yayınlanmış iletişim bilgisi ister.

→ Bildirim akışı `destek.html` / `en/support.html` sayfalarına eklendi.
Uygulama tarafında da aynı mekanizmanın bulunması gerekir.

---

## D. Yazım düzeltmeleri

Belgelerdeki içerik korunmuş, yalnızca tartışmasız yazım ve boşluk hataları
düzeltilmiştir. Düzeltmelerin tam listesi `tools/build_legal.py` içindeki
`TYPO_FIXES` dizisinde; hangi düzeltmenin kaç kez uygulandığını görmek için:

```bash
python3 tools/build_legal.py /kaynak/docx/klasoru
```

Örnekler: `işllenmemekedir → işlenmektedir`, `sahptirler → sahiptirler`,
`YŞipşak Ye → Şipşak Ye`, `çözümündeAntalya → çözümünde Antalya`,
`Kanun'unilgili → Kanun'un ilgili`, noktalama öncesi fazla boşlukların kaldırılması.

---

## Özet öncelik sırası

| Öncelik | Madde | Neden |
|---------|-------|-------|
| 1 | A1 — Künye | Yasal zorunluluk + mağaza reddi |
| 2 | C2 — Üçüncü taraf servisler ve yurt dışı aktarım | Mağaza reddinin 1 numaralı sebebi |
| 3 | C3 — Hesap silme akışının uygulamayla uyumu | Play ve Apple zorunluluğu |
| 4 | A2, A3 — Cayma hakkı ve ön bilgilendirme formu | Yasal zorunluluk |
| 5 | B1, B2 — Haksız şart riski | Tüketici şikâyeti riski |
| 6 | A4, A5 — Eksik madde numaraları | Belge bütünlüğü |
| 7 | C1 — İYS onayı | Push pazarlama yapılacaksa zorunlu |
| 8 | B3, B4 — Yetki ve FSEK maddeleri | Gözden geçirilmeli |
