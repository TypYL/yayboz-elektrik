# Yayboz Elektrik & Otomasyon

Türkçe, mobil uyumlu şirket tanıtım sitesi. Elektrik ve elektronik mühendisliği, proje ve taahhüt, otomasyon, pano imalatı ve montajı, sanayi/konut tesisatları, arıza teşhis, bakım, servis, malzeme alım satımı ve revizyon hizmetlerini kapsar.

Canlı site: **https://yayboz-elektrik.web.app/**

Firebase projesi ve Hosting sitesi: `yayboz-elektrik`. Kaynak kodu: https://github.com/TypYL/yayboz-elektrik

## Yapı

- `dist/`: Yayımlanabilir statik site. Sunucu veya paket kurulumu gerektirmez.
- `scripts/build.py`: İncelenmiş içerik, 9 hizmet ve 34 proje kaydından sayfaları üretir.
- `dist/styles.css`, `dist/app.js`: Lacivert, çelik grisi ve ölçülü turuncu tasarım; galeri, filtre ve iletişim etkileşimleri.
- `scripts/sections/automation.html`, `dist/automation.css`, `dist/automation.js`: Başlat/durdur ve kontaktör mühürleme devresinin etkileşimli SVG gösterimi.
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

Altı kartlık uygulama bölümündeki yenilenmiş fotoğraflar, özgün proje referanslarına göre yapay zekâ ile oluşturulmuş ve “Görsel canlandırma” etiketiyle belirtilmiştir. Pano içi ve HMI görüntüleri özgün sunumdandır. Her kart özgün PowerPoint görsellerini açar. Ana sayfa kapağı ve Hakkımızda bölümündeki tesis fotoğrafı temsili görsellerdir. Yeni üretilen fotoğrafların doğal çözünürlüğü 1672 × 941 pikseldir; 800 piksel genişliğinde mobil varyantları da sunulur. 4K/UHD oldukları iddia edilmez. Üretim komutları ve kaynak bilgileri `ASSET_SOURCES.json` dosyasındadır.

Kumanda devresi animasyonu tarayıcı içinde çalışır. Başlatma, kontaktörün çekmesi, yardımcı kontağın devreyi tutması ve durdurma aşamalarını gösterir. Otomatik gösterim duraklatılabilir; ekran dışında veya sekme gizliyken durur. İşletim sisteminin hareket azaltma tercihinde otomatik hareket kapalıdır, düğmeler statik durumları değiştirmeye devam eder. Fiziksel donanıma bağlı değildir; şema temsili gösterim içindir.

Kaynak sunumdaki harici video dosyaları siteye dahil değildir. Simülasyon ve eğitim projeleri işaretlenmiştir.

## Doğrulama

`scripts/check_browser.py`, Playwright ve Chromium ile telefon/masaüstü düzenini, proje filtrelerini, galeri kontrollerini, klavye erişimini ve WhatsApp mesaj hazırlamayı kontrol eder. Gerçek WhatsApp mesajı göndermez. Yerel araçlar, kaynak PowerPoint ve QA ekran görüntüleri Git'e alınmaz.

`scripts/check_visual_refresh.py`, altı kartı, görsel etiketlerini, animasyonun başlat/durdur ve otomatik akışını, motor hareketini, ekran dışında duraklatmayı, hareket azaltma tercihini ve masaüstü/telefon erişilebilirliğini kontrol eder. `YAYBOZ_QA_URL` verilirse aynı kontrolleri canlı adreste çalıştırır.

İşletmeye ait içerik ve proje görsellerinin hakları ilgili sahiplerine aittir. Manrope yazı tipi SIL Open Font License ile kullanılır; lisansı `dist/assets/Manrope-LICENSE.txt` içindedir.
