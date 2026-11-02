# Yayboz Elektrik & Otomasyon

Türkçe, mobil uyumlu şirket tanıtım sitesi. Elektrik ve elektronik mühendisliği, proje ve taahhüt, otomasyon, pano imalatı ve montajı, sanayi/konut tesisatları, arıza teşhis, bakım, servis, malzeme alım satımı ve revizyon hizmetlerini kapsar.

## Yapı

- `dist/`: Yayımlanabilir statik site. Sunucu veya paket kurulumu gerektirmez.
- `scripts/build.py`: İncelenmiş içerik, 9 hizmet ve 34 proje kaydından sayfaları üretir.
- `dist/styles.css`, `dist/app.js`: Tasarım ve tarayıcı etkileşimleri.
- `firebase.json`: Firebase Hosting yapılandırması; yayımlanacak klasör `dist`.
- `ASSET_SOURCES.json`: Görsel kaynakları, temsili kapak görselinin üretim bilgisi.

## Yerel önizleme

```sh
python3 scripts/build.py
python3 -m http.server 8769 --bind 127.0.0.1 --directory dist
```

## Yayın

Kaynak kodu `main` dalında tutulur. `gh-pages` dalı yalnızca `dist` içeriğini barındırır. GitHub Pages ayarı `gh-pages /` şeklindedir.

Firebase Hosting için hesap oturumu açıldıktan sonra ilgili Firebase projesi seçilir ve aşağıdaki komutla yalnızca Hosting yayımlanır:

```sh
firebase login
firebase deploy --only hosting --project YOUR_PROJECT_ID
```

Firebase hesabı/projesi oluşturulması ve yayın sonucu ayrıca doğrulanmalıdır. `firebase.json` dosyasının bulunması tek başına Firebase'e yayın yapıldığı anlamına gelmez. Firebase alan adına geçildiğinde `scripts/build.py` içindeki `BASE` adresi güncellenip sayfalar yeniden üretilir. Ücretsiz Hosting kullanım kotasına tabidir; ücretli plan veya özel alan adı satın alımı bu depoya dahil değildir.

## İçerik ve iletişim

Firma, 30 yıllık tecrübe ve mühendis kadrosu bilgileriyle tanıtılır. İsimler, telefonlar ve adres sağlanan kartvizitten; proje listesi kullanıcı metni ve sunumdan alınmıştır. E-posta adresi, çalışma saatleri, müşteri yorumları ve sertifikalar eklenmemiştir.

Form, kullanıcının metnini WhatsApp bağlantısına ekler; mesajı ziyaretçi WhatsApp içinde gönderir. Site form verisi saklamaz. İstatistik izleyici ve reklam çerezi yoktur. Yazı tipleri ve görseller yerel olarak sunulur.

Proje fotoğrafları ve teknik ekran görüntüleri özgün PowerPoint görsellerinden web için dönüştürülmüştür. Ana sayfadaki endüstriyel kapak yapay zekayla üretilmiş temsili görseldir; gerçek proje kanıtı olarak sunulmaz. Kaynak sunumdaki harici video dosyaları siteye dahil değildir. Simülasyon ve eğitim projeleri işaretlenmiştir.

## Doğrulama

`scripts/check_browser.py`, Playwright ve Chromium ile telefon/masaüstü düzenini, proje filtrelerini, galeri kontrollerini, klavye erişimini ve WhatsApp mesaj hazırlamayı kontrol eder. Gerçek WhatsApp mesajı göndermez. Yerel araçlar, kaynak PowerPoint ve QA ekran görüntüleri Git'e alınmaz.

İşletmeye ait içerik ve proje görsellerinin hakları ilgili sahiplerine aittir. Manrope yazı tipi SIL Open Font License ile kullanılır; lisansı `dist/assets/Manrope-LICENSE.txt` içindedir.
