# Yayına alma — Ubuntu VPS + Cloudflare

Site tamamen statik: derleme adımı yok, çalışma zamanı bağımlılığı yok.
Nginx dosyaları doğrudan servis eder.

---

## 1. Sunucu hazırlığı

```bash
sudo apt update && sudo apt install -y nginx git
sudo mkdir -p /var/www/sipsakye.com
sudo chown -R $USER:$USER /var/www/sipsakye.com
```

## 2. Depoyu sunucuya çek

```bash
git clone <depo-adresi> /var/www/sipsakye.com
cd /var/www/sipsakye.com
git checkout claude/mobile-app-promo-site-yecg4a
```

> Depo özel ise sunucuda bir **deploy key** oluşturup (`ssh-keygen -t ed25519`)
> genel anahtarı GitHub'da deponun *Settings → Deploy keys* bölümüne ekleyin.

## 3. Cloudflare DNS

Cloudflare panelinde alan adınız için:

| Tür | Ad | İçerik | Proxy |
|-----|----|--------|-------|
| A | `@` | VPS IPv4 adresi | Proxied (turuncu bulut) |
| A | `www` | VPS IPv4 adresi | Proxied (turuncu bulut) |

## 4. TLS — Cloudflare Origin Certificate (önerilen)

Cloudflare panelinde **SSL/TLS → Origin Server → Create Certificate**:

* Hostname: `sipsakye.com`, `*.sipsakye.com`
* Geçerlilik: 15 yıl

Üretilen sertifika ve anahtarı sunucuya yazın:

```bash
sudo mkdir -p /etc/ssl/cloudflare
sudo nano /etc/ssl/cloudflare/sipsakye.com.pem   # Origin Certificate
sudo nano /etc/ssl/cloudflare/sipsakye.com.key   # Private Key
sudo chmod 600 /etc/ssl/cloudflare/sipsakye.com.key
```

Ardından Cloudflare'de **SSL/TLS → Overview → Full (strict)** seçin.

> **Flexible modda bırakmayın.** Flexible, Cloudflare ile sunucunuz arasındaki
> trafiği şifresiz bırakır ve nginx'teki HTTPS yönlendirmesiyle birlikte
> sonsuz yönlendirme döngüsüne yol açar.

**Alternatif — Let's Encrypt:** Cloudflare proxy'yi geçici olarak kapatın
(gri bulut), `sudo apt install certbot python3-certbot-nginx` ve
`sudo certbot --nginx -d sipsakye.com -d www.sipsakye.com` çalıştırın,
sonra proxy'yi tekrar açın. `deploy/nginx.conf` içindeki sertifika yollarını
`/etc/letsencrypt/live/...` olarak güncelleyin.

## 5. Cloudflare ek ayarları

* **SSL/TLS → Edge Certificates → Always Use HTTPS:** açık
* **Speed → Optimization → Brotli:** açık
* **Caching → Configuration → Browser Cache TTL:** *Respect Existing Headers*
* **Rules → Page Rules / Cache Rules:** `sipsakye.com/*.html` için *Bypass cache*
  ya da kısa TTL — hukuki metin güncellendiğinde eski sürüm servis edilmesin.

## 6. Nginx yapılandırması

```bash
sudo cp /var/www/sipsakye.com/deploy/nginx.conf /etc/nginx/sites-available/sipsakye.com
sudo ln -s /etc/nginx/sites-available/sipsakye.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` hata verirse çıktıdaki satır numarasına bakın; en sık sebep
sertifika dosyalarının henüz yazılmamış olmasıdır.

## 7. Güncelleme akışı

Yerelde değişiklik yapıp push edin, sonra sunucuda:

```bash
cd /var/www/sipsakye.com && ./deploy/update.sh
```

Ya da doğrudan:

```bash
cd /var/www/sipsakye.com && git pull origin claude/mobile-app-promo-site-yecg4a
```

Nginx'i yeniden başlatmaya gerek yok — dosyalar diskten okunur.
Cloudflare önbelleğini temizlemek isterseniz panelden
**Caching → Configuration → Purge Everything**.

## 8. Güvenlik duvarı

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

İsterseniz 80/443 portlarını yalnızca Cloudflare IP aralıklarına açarak
origin'i doğrudan erişime kapatabilirsiniz — güncel liste
<https://www.cloudflare.com/ips/> adresinde.

---

## Yayına almadan önce kontrol listesi

```bash
python3 tools/check_placeholders.py   # doldurulmamış künye alanları
python3 tools/check_links.py          # kırık iç bağlantı
```

Ayrıntılı mağaza kontrol listesi için depodaki `MAGAZA-KONTROL.md` dosyasına bakın.
