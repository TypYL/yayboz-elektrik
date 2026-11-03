# Yayboz Elektrik & Otomasyon

Türkçe, mobil uyumlu şirket tanıtım sitesi. Elektrik ve elektronik mühendisliği, proje ve taahhüt, otomasyon, pano imalatı ve montajı, sanayi/konut tesisatları, arıza teşhis, bakım, servis, malzeme alım satımı ve revizyon hizmetlerini kapsar.

Canlı site: **https://yayboz-elektrik.web.app/**

Firebase projesi ve Hosting sitesi: `yayboz-elektrik`. Kaynak kodu: https://github.com/TypYL/yayboz-elektrik

## Yapı

- `dist/`: Yayımlanabilir statik site. Sunucu veya paket kurulumu gerektirmez.
- `scripts/build.py`: İncelenmiş içerik, 9 hizmet ve 34 proje kaydından sayfaları üretir.
- `dist/styles.css`, `dist/app.js`: Tasarım ve tarayıcı etkileşimleri.
- `firebase.json`: Firebase Hosting yapılandırması; yayımlanacak klasör `dist`.
- `.firebaserc`: Kullanıcının oluşturduğu `yayboz-elektrik` Firebase projesi seçimi.
- `ASSET_SOURCES.json`: Görsel kaynakları, temsili kapak görselinin üretim bilgisi.

## Yerel önizleme

```sh
python3 scripts/build.py
python3 -m http.server 8769 --bind 127.0.0.1 --directory dist
```

## Yayın

Kaynak kodu `main` dalında tutulur. Ana yayın Firebase Hosting üzerindedir. `gh-pages` dalı yalnızca `dist` içeriğini barındırır; GitHub Pages kopyasının ayarı `gh-pages /` şeklindedir. Canonical adres ve site haritası Firebase adresini işaret eder.

Firebase Hosting'e güncelleme için hesap oturumu açıkken içerik üretilir ve yalnızca Hosting yayımlanır:

```sh
firebase login
python3 scripts/build.py
firebase deploy --only hosting --project yayboz-elektrik
```

Firebase yayını 3 Kasım 2026 tarihinde tamamlandı. Projede ücretli faturalandırma kapalıdır ve fatura hesabı bağlı değildir. Ücretsiz Hosting kullanım kotasına tabidir. Özel alan adı satın alınmadı; `yayboz-elektrik.web.app` Firebase'in sağladığı HTTPS adresidir. Dağıtım kimlik bilgileri ve hesap oturumları bu depoda tutulmaz.

Kurulum sırasında kullanılan `yayboz.web.app` adresi ana adrese 302 yönlendirmesi yapar. Bu ayrı yönlendirme `firebase.redirect.json` ile, yalnızca `yayboz` projesine yayımlanır; normal `firebase deploy` hedefi `yayboz-elektrik` olarak kalır.

## İçerik ve iletişim

Firma, 30 yıllık tecrübe ve mühendis kadrosu bilgileriyle tanıtılır. İsimler, telefonlar ve adres sağlanan kartvizitten; proje listesi kullanıcı metni ve sunumdan alınmıştır. E-posta adresi, çalışma saatleri, müşteri yorumları ve sertifikalar eklenmemiştir.

Form, kullanıcının metnini WhatsApp bağlantısına ekler; mesajı ziyaretçi WhatsApp içinde gönderir. Site form verisi saklamaz. İstatistik izleyici ve reklam çerezi yoktur. Yazı tipleri ve görseller yerel olarak sunulur.

Proje fotoğrafları ve teknik ekran görüntüleri özgün PowerPoint görsellerinden web için dönüştürülmüştür. Ana sayfadaki endüstriyel kapak yapay zekayla üretilmiş temsili görseldir; gerçek proje kanıtı olarak sunulmaz. Kaynak sunumdaki harici video dosyaları siteye dahil değildir. Simülasyon ve eğitim projeleri işaretlenmiştir.

## Doğrulama

`scripts/check_browser.py`, Playwright ve Chromium ile telefon/masaüstü düzenini, proje filtrelerini, galeri kontrollerini, klavye erişimini ve WhatsApp mesaj hazırlamayı kontrol eder. Gerçek WhatsApp mesajı göndermez. Yerel araçlar, kaynak PowerPoint ve QA ekran görüntüleri Git'e alınmaz.

İşletmeye ait içerik ve proje görsellerinin hakları ilgili sahiplerine aittir. Manrope yazı tipi SIL Open Font License ile kullanılır; lisansı `dist/assets/Manrope-LICENSE.txt` içindedir.
