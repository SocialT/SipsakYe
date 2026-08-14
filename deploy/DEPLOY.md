# Yayına alma — mevcut Docker + Caddy altyapısı

Bu sunucuda zaten Şipşak Ye backend'i Docker Compose ile çalışıyor
(`sipsakye-caddy`, `sipsakye-api`, `sipsakye-web`, Redis, Postgres — `sipsakye`
adlı Docker ağında). Tanıtım sitesi bu altyapıya **ayrı, küçük bir statik-dosya
container'ı** olarak eklenir; mevcut servislere dokunulmaz. TLS ve
`sipsakye.com` yönlendirmesini zaten çalışan Caddy üstlenir.

Site tamamen statik: derleme adımı yok, çalışma zamanı bağımlılığı yok.

---

## 1. Depoyu sunucuya çek

```bash
mkdir -p /var/www/sipsakye.com
git clone https://github.com/SocialT/SipsakYe.git /var/www/sipsakye.com
cd /var/www/sipsakye.com
git checkout claude/mobile-app-promo-site-yecg4a
```

Depo herkese açık (public), ekstra deploy key/token gerekmez.

> Site şu an `claude/mobile-app-promo-site-yecg4a` dalında hazır; henüz
> `main`'e birleştirilmedi. `main`'e alındığında sunucuda
> `git checkout main && git pull` ile geçebilirsiniz.

## 2. Tanıtım sitesi container'ını ayağa kaldır

```bash
cd /var/www/sipsakye.com
docker compose -f deploy/docker-compose.promo.yml up -d
```

Bu, `sipsakye-promo` adında yeni bir `nginx:alpine` container'ı açar, repo
kökünü salt-okunur mount eder ve mevcut `sipsakye` Docker ağına bağlar —
**80/443 portlarını dinlemez**, dışarıdan doğrudan erişilemez. Sadece Caddy
container-içi ağdan `sipsakye-promo:80` adresine ulaşabilir.

Kontrol:

```bash
docker ps --filter name=sipsakye-promo
docker logs sipsakye-promo
```

## 3. Caddy'ye sipsakye.com'u tanıt

Caddy yapılandırması `/root/sipsakye/backend/SepetifyGoBackend/deploy/Caddyfile`
dosyasında. Şu iki bloğu **mevcut `api.sipsakye.com` / `admin.sipsakye.com`
bloklarının yanına** ekleyin (silmeyin, üstüne eklemeyin):

```caddyfile
www.sipsakye.com {
        redir https://sipsakye.com{uri} permanent
}

sipsakye.com {
        reverse_proxy sipsakye-promo:80 {
                header_up Host {host}
                header_up X-Real-IP {remote_host}
                header_up X-Forwarded-For {remote_host}
                header_up X-Forwarded-Proto {scheme}
        }
}
```

```bash
nano /root/sipsakye/backend/SepetifyGoBackend/deploy/Caddyfile
```

Kaydettikten sonra Caddy'yi yeniden yükleyin (container'ı yeniden
başlatmadan, sıfır kesintili config reload):

```bash
docker exec sipsakye-caddy caddy reload --config /etc/caddy/Caddyfile
```

`admin.sipsakye.com` ve `api.sipsakye.com` bloklarına dokunmadığınız için bu
işlem onları etkilemez.

Caddy, `sipsakye.com` ve `www.sipsakye.com` için otomatik olarak Let's
Encrypt sertifikası alıp yenileyecek — `api`/`admin` için zaten yaptığı gibi.
Ayrıca Cloudflare Origin Certificate oluşturduysanız (`/etc/ssl/cloudflare/`
altında), bu akışta **kullanılmıyor** — isterseniz sunucudan silebilirsiniz,
zararsız da durabilir.

## 4. Cloudflare DNS

Cloudflare panelinde alan adınız için:

| Tür | Ad | İçerik | Proxy |
|-----|----|--------|-------|
| A | `@` | `167.233.54.178` | Proxied (turuncu bulut) |
| A | `www` | `167.233.54.178` | Proxied (turuncu bulut) |

`api` ve `admin` alt alan adları muhtemelen zaten benzer şekilde tanımlı;
onlara dokunmayın.

## 5. Cloudflare SSL/TLS modu

**SSL/TLS → Overview → Full (strict)** seçin. Caddy origin'de geçerli,
herkesçe güvenilir bir Let's Encrypt sertifikası sunacağı için bu güvenle
çalışır.

> **Flexible modda bırakmayın** — Cloudflare ile sunucu arasındaki trafiği
> şifresiz bırakır.

Eğer `sipsakye.com` proxy'li (turuncu bulut) durumdayken Caddy ilk
sertifikayı alamazsa (loglarda `no bind()`/ACME hata görürseniz), bir kerelik
şu yolu deneyin: DNS kaydını geçici olarak **DNS only** (gri bulut) yapın,
birkaç dakika bekleyip `docker logs sipsakye-caddy` ile sertifikanın
alındığını doğrulayın, sonra tekrar **Proxied** yapın.

## 6. Cloudflare ek ayarları

* **SSL/TLS → Edge Certificates → Always Use HTTPS:** açık
* **Speed → Optimization → Brotli:** açık
* **Caching → Configuration → Browser Cache TTL:** *Respect Existing Headers*
* **Rules → Page Rules / Cache Rules:** `sipsakye.com/*.html` için *Bypass cache*
  ya da kısa TTL — hukuki metin güncellendiğinde eski sürüm servis edilmesin.

## 7. Güncelleme akışı

Yerelde değişiklik yapıp push edin, sonra sunucuda:

```bash
cd /var/www/sipsakye.com
git pull origin claude/mobile-app-promo-site-yecg4a
docker compose -f deploy/docker-compose.promo.yml restart
```

Caddy'yi yeniden başlatmaya gerek yok — sadece Caddyfile değiştiğinde
`docker exec sipsakye-caddy caddy reload --config /etc/caddy/Caddyfile`
yeterli. Cloudflare önbelleğini temizlemek isterseniz panelden
**Caching → Configuration → Purge Everything**.

---

## Alternatif: Docker/Caddy olmadan, doğrudan native nginx

Bu sunucuda zaten Docker + Caddy çalıştığı için yukarıdaki yol önerilir.
Docker kullanmayan **farklı** bir sunucuya kurulum yapacaksanız `deploy/nginx.conf`
(host'ta doğrudan çalışan, kendi TLS'ini Cloudflare Origin Certificate ile
sağlayan tam sürüm) ve `deploy/update.sh` dosyalarını kullanın:

```bash
sudo apt update && sudo apt install -y nginx git
git clone https://github.com/SocialT/SipsakYe.git /var/www/sipsakye.com
sudo cp /var/www/sipsakye.com/deploy/nginx.conf /etc/nginx/sites-available/sipsakye.com
sudo ln -s /etc/nginx/sites-available/sipsakye.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
# /etc/ssl/cloudflare/ altına Cloudflare Origin Certificate'ı yazın (bkz. Caddy
# bölümündeki adım 3'ün Cloudflare tarafı), sonra:
sudo nginx -t && sudo systemctl reload nginx
```

## 8. Güvenlik duvarı

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'   # ya da Docker/Caddy kurulumunda: 80,443/tcp
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
