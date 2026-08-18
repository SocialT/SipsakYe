# Şipşak Ye — Web

Bu repo Şipşak Ye'nin web varlıklarını barındırır.

## Hesap Silme Sayfası (`/hesap-sil`)

`hesap-sil/index.html`, kullanıcıların uygulamayı açmadan, sadece telefon + SMS OTP
doğrulamasıyla hesaplarını ve kişisel verilerini kalıcı olarak silebilmesi için
Apple/Google mağaza politikaları gereği eklenen tek sayfalık, framework'süz bir
web sayfasıdır. Build adımı yok — statik dosya olarak herhangi bir hosting'e
(Nginx, GitHub Pages, Vercel/Netlify static) doğrudan deploy edilebilir.

Backend: `SocialT/SepetifyGoBackend` — `POST /api/v1/user/account-deletion/start`
ve `POST /api/v1/user/account-deletion/verify` (auth gerektirmez).

### Deploy öncesi kontrol edilmesi gerekenler

1. **API base URL** — `hesap-sil/index.html` başındaki `API_BASE_URL` sabiti,
   backend'in gerçek prod domain'ine göre güncellenmeli (bu PR yazılırken API'nin
   public domain'i teyit edilemedi, `https://api.sipsakye.com` placeholder olarak
   bırakıldı).
2. **CORS** — Backend `APP_ALLOWED_ORIGINS` ortam değişkeni, bu sayfanın
   yayınlanacağı origin'i (örn. `https://sipsakye.com`) içermeli. Sayfa
   `https://sipsakye.com` altında (örn. `/hesap-sil`) yayınlanırsa ek bir şey
   gerekmez; farklı bir origin/subdomain kullanılacaksa backend'in prod `.env`
   dosyasındaki `APP_ALLOWED_ORIGINS` listesine eklenmeli.
