#!/usr/bin/env python3
"""Build the portable, dependency-free Yayboz website from reviewed content."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
BASE = 'https://yayboz-elektrik.web.app/'
ICONS = {
 'arrow':'<path d="M5 12h14m-6-6 6 6-6 6"/>',
 'up':'<path d="M6 18 18 6M6 6h12v12"/>',
 'phone':'<path d="m7 3 3 5-3 3a15 15 0 0 0 6 6l3-3 5 3-1 4C10 23 1 14 3 4z"/>',
 'pin':'<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'bolt':'<path d="m13 2-9 12h7l-1 8 10-13h-8z"/>',
 'circuit':'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"/><path d="M10 10h4v4h-4z"/>',
 'panel':'<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 7h8M8 12h8M8 17h3m5-1v2"/>',
 'factory':'<path d="M3 21V10l6 3V9l6 3V3h5l1 18H3Z"/><path d="M7 17v1m5-1v1m5-1v1"/>',
 'tools':'<path d="m14 6 4-4a6 6 0 0 0-7 8l-8 8a2 2 0 0 0 3 3l8-8a6 6 0 0 0 8-7l-4 4-4-4Z"/>',
 'box':'<path d="m12 2 9 5v10l-9 5-9-5V7l9-5Zm0 10v10M3 7l9 5 9-5M7 4.8l10 5.5v5"/>',
 'plan':'<path d="M4 3h11l5 5v13H4zM14 3v6h6M8 13h8m-8 4h5"/>',
 'refresh':'<path d="M20 7a9 9 0 0 0-15-2L2 8m0-6v6h6M4 17a9 9 0 0 0 15 2l3-3m0 6v-6h-6"/>',
 'check':'<path d="m5 12 4 4L19 6"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'message':'<path d="M21 11.5a9 9 0 0 1-13 8L3 21l1.5-5a9 9 0 1 1 16.5-4.5Z"/><path d="M8 8c0 4 4 8 8 8l1-3-3-1-1 1-2-2 1-1-1-3-3 1Z"/>',
 'close':'<path d="m6 6 12 12M6 18 18 6"/>',
 'menu':'<path d="M4 6h16M4 12h16M4 18h16"/>',
}
def icon(name, cls=''):
 return f'<svg class="icon {cls}" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
def logo():
 return '<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 48 60"><path d="m27 0-25 38 18-9-1 31 27-42-19 10z" fill="currentColor"/></svg></span><span class="brand-type"><strong>YAY<span>BOZ</span></strong><small>ELEKTRİK & OTOMASYON</small></span>'

services = [
 ('plan','Mühendislik, proje & taahhüt','Mühendis kadromuzla elektrik ve elektronik projelendirme, teknik planlama ve uygulama taahhüdü.'),
 ('circuit','Otomasyon sistemleri','PLC, HMI ve SCADA uygulamaları; makine ve üretim süreçlerine özel kontrol sistemleri.'),
 ('panel','Pano imalatı & montajı','Dağıtım, kumanda ve kompanzasyon panolarının projelendirilmesi, imalatı ve montajı.'),
 ('factory','Sanayi & fabrika tesisatları','Sanayi bölgeleri ve üretim tesisleri için elektrik altyapısı, makine bağlantıları ve saha uygulamaları.'),
 ('bolt','Konut & iş yeri tesisatları','Ev, ofis ve ticari alanlarda elektrik tesisatı, aydınlatma ve elektrik altyapısının yenilenmesi.'),
 ('tools','Arıza teşhis, bakım & servis','Elektrik ve otomasyon sistemlerinde arıza tespiti, periyodik bakım, onarım ve teknik servis.'),
 ('box','Malzeme alım & satımı','Elektrik ve otomasyon malzemelerinin alım satımı; projenize uygun ürün ve ekipman tedariği.'),
 ('refresh','Tadilat & revizyon','Mevcut panoların, makinelerin ve tesisatların ihtiyaca göre yenilenmesi ve modernizasyonu.'),
 ('plan','Elektrik proje çizimi','Makine ve tesislere ait elektrik devre şemaları, pano çizimleri ve uygulama projeleri.'),
]
projects = []
def project(title, category, slides=(), note='', desc=''):
 projects.append(dict(id=f'p{len(projects)+1:02}',title=title,category=category,slides=list(slides),note=note,description=desc))
auto='Otomasyon sistemleri';siemens='Siemens TIA Portal / WinCC';drawing='Elektrik devresi proje çizimleri'
project('KEYENCE ve PLC ile ilaç kutularında Lot No ve SKT kontrolü',auto)
project('Etiket makinesi otomasyon sistemi',auto)
project('Pnömatik oransal regülatörlü pres otomasyonu',auto)
project('Contalı ve pnömatik yat kapısı otomasyonu',auto)
project('Kağıt helva makinesi otomasyonu',auto)
project('Dikey sac kumlama makinesi otomasyon sistemi',auto,[3,4,5,6],desc='Motor sürücüleri, Modbus RTU haberleşmesi ve kumanda panosuyla dikey sac kumlama makinesi kontrolü.')
project('Endüstriyel datalogger — beyaz eşya ölçüm istasyonu',auto,[8,9,10,11,12,13,14],desc='Enerji, sıcaklık, basınç, nem ve debi verilerinin kaydedilmesi; HMI üzerinden izleme ve veri dışa aktarma.')
project('Folyo dilimleme makinesi',auto,[16,17,18,19],desc='Motor ve sürücü kontrolü, kesim ayarları, uzunluk takibi ve HMI operatör ekranları.')
project('120 ton eksantrik pres',auto,[26,27],desc='PLC tabanlı pres kontrolü, çalışma modları ve proje sunumunda yer alan kontrol mantığı.')
project('Step motor ile oyuk açma makinesi',auto,[20])
project('PID ile fileleme makinesi',auto,[21,22,23,24],desc='Ürün fileleme sürecinde sıcaklık kontrolü, konveyör ve kesim adımlarının otomasyonu.')
project('Yağ ayrıştırma makinesi SCADA',auto,[37])
project('Friksiyon pres revizyonu',auto)
project('Kulp basma makinesi — hidrolik pres',auto,[45])
project('Mezuniyet projesi',auto,[32,33,34,35],note='Eğitim projesi',desc='PLC ve HMI ile notaların işlenmesi ve elektronik org kontrolü üzerine mezuniyet çalışması.')
project('Bilgi yarışması standı',auto,[47])
project('Çeşitli otomasyon projeleri',auto,[48,49])
project('Excel otomasyonları — veri işleme',auto)
project('Çapak alma makinesi',siemens,[44])
project('Asansör otomasyon sistemi',siemens,[38],note='Simülasyon')
project('Eş yaşlandırma projesi',siemens,[40],note='Simülasyon')
project('Motor yol verme modları',siemens)
project('Havuz sistemi',siemens,[42],note='Simülasyon')
for title,slides in [
 ('PKM 80 mekanik montaj makinesi',[49]),('Teker sıvama makinesi',[]),
 ('Alüminyum profil bükme makinesi — çatılar için',[]),('Kumaş yapıştırma makinesi',[]),
 ('17 valfli patlaç',[]),('Perçinleme makinesi',[29,30]),('Kağıt helva makinesi',[]),
 ('Yuvarlak profil delme makinesi',[]),('Kauçuk pişirme makinesi — hidrolik',[]),
 ('Perçin çakma projesi',[]),('Çift kapaklı kumlama makinesi',[])]:
 project(title,drawing,slides)

(DIST/'assets/projects.json').write_text(json.dumps(projects,ensure_ascii=False,indent=2))
service_html=''.join(f'<article class="service"><div class="service-top">{icon(i)}<span>0{n+1}</span></div><h3>{t}</h3><p>{d}</p></article>' for n,(i,t,d) in enumerate(services))
featured=[(projects[6],8,'measure'),(projects[7],16,'slitter'),(projects[5],3,'blaster')]
featured_html=''.join(f'''<button type="button" class="project-card" data-project="{p['id']}" aria-label="{escape(p['title'])}: görselleri incele"><div class="project-photo {c}"><img src="assets/proje-{n:02}.webp" width="1920" height="1080" loading="lazy" alt="{escape(p['title'])} projesinin sunumundaki gerçek makine fotoğrafı"><span class="view-label">Görselleri incele {icon('up')}</span></div><div class="project-info"><span class="eyebrow">{('ÖLÇÜM & VERİ TOPLAMA' if n==8 else 'MAKİNE OTOMASYONU')}</span><h3>{p['title']}</h3><p>{p['description']}</p></div></button>''' for p,n,c in featured)
catalog=''
for cat in [auto,siemens,drawing]:
 subset=[p for p in projects if p['category']==cat]
 rows=''
 for p in subset:
  label=f'<span>{escape(p["title"])}'+(f'<small class="tag">{p["note"]}</small>' if p['note'] else '')+'</span>'
  rows+=f'<li class="catalog-item" data-category="{escape(cat)}" data-title="{escape(p["title"])}"><span class="item-number">{p["id"][1:]}</span>'+(f'<button type="button" data-project="{p["id"]}">{label}<span class="item-action">Görseller {icon("up")}</span></button>' if p['slides'] else f'<div>{label}{icon("check","list-check")}</div>')+'</li>'
 catalog+=f'<section class="catalog-group" data-group="{escape(cat)}"><h3>{cat}<span>{len(subset):02}</span></h3><ul>{rows}</ul></section>'
schema={"@context":"https://schema.org","@type":"Electrician","name":"Yayboz Elektrik & Otomasyon","url":BASE,"image":BASE+'assets/paylasim.jpg',"telephone":"+902164990983","description":"30 yıllık tecrübe ve mühendis kadrosuyla elektrik, elektronik, otomasyon, proje ve taahhüt hizmetleri.","address":{"@type":"PostalAddress","streetAddress":"4. Esenşehir Mahallesi, Atılım Sokak No:42/2, Yukarı Dudullu","addressLocality":"Ümraniye","addressRegion":"İstanbul","addressCountry":"TR"},"areaServed":{"@type":"City","name":"İstanbul"},"contactPoint":[{"@type":"ContactPoint","telephone":"+905359685560","contactType":"customer service","availableLanguage":"Turkish"},{"@type":"ContactPoint","telephone":"+905333268092","contactType":"customer service","availableLanguage":"Turkish"}]}
html=f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#321649">
<title>Yayboz Elektrik & Otomasyon | Mühendislik, Proje ve Taahhüt</title>
<meta name="description" content="Yayboz Elektrik: 30 yıllık tecrübe ve mühendis kadrosuyla Ümraniye'de elektrik, otomasyon, pano imalatı, proje taahhüt, tesisat, bakım ve servis.">
<link rel="canonical" href="{BASE}"><meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:title" content="Yayboz Elektrik & Otomasyon"><meta property="og:description" content="30 yıllık tecrübe. Mühendislikten uygulamaya, elektrik ve otomasyonda çözüm ortağınız."><meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}assets/paylasim.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"><link rel="preload" as="image" href="assets/endustri-hero.webp" fetchpriority="high">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="app.js" defer></script></head>
<body><a class="skip-link" href="#icerik">İçeriğe geç</a>
<div class="topbar"><div class="container"><span>{icon('pin')} Yukarı Dudullu, Ümraniye / İstanbul</span><a href="tel:+902164990983">{icon('phone')} 0216 499 09 83</a></div></div>
<header class="site-header"><div class="container header-inner"><a class="brand" href="#ana-sayfa" aria-label="Yayboz Elektrik ana sayfa">{logo()}</a><button class="menu-toggle" type="button" aria-label="Menüyü aç" aria-controls="main-nav" aria-expanded="false">{icon('menu')}</button><nav id="main-nav" aria-label="Ana gezinme"><a href="#ana-sayfa" class="active">Ana Sayfa</a><a href="#hakkimizda">Hakkımızda</a><a href="#hizmetler">Hizmetler</a><a href="#projeler">Projeler</a><a href="#iletisim">İletişim</a><a href="#iletisim" class="button nav-cta">Projenizi konuşalım {icon('up')}</a></nav></div></header>
<main id="icerik"><section class="hero" id="ana-sayfa" aria-labelledby="hero-title"><img class="hero-image" src="assets/endustri-hero.webp" width="1672" height="941" alt="Endüstriyel otomasyon ve elektrik panolarını gösteren temsili tesis görseli" fetchpriority="high"><div class="hero-shade"></div><div class="container hero-content"><p class="eyebrow light"><span></span> YAYBOZ ELEKTRİK & OTOMASYON</p><h1 id="hero-title">Gücünüzü<br>tecrübeyle<br><em>buluşturuyoruz.</em></h1><p class="hero-description">30 yıllık tecrübe ve mühendis kadromuzla;<br class="desktop-break"> projeden uygulamaya, elektrikten otomasyona.</p><div class="hero-actions"><a class="button" href="#hizmetler">Hizmetlerimizi keşfedin {icon('arrow')}</a><a class="text-link light" href="#projeler">Projelerimiz {icon('up')}</a></div><div class="hero-bottom"><span>{icon('check')} Mühendislik & taahhüt</span><span>{icon('check')} Sanayi, ticari alanlar & konut</span></div></div><span class="image-note">Temsili endüstriyel görsel</span><a class="scroll-hint" href="#hakkimizda" aria-label="Hakkımızda bölümüne ilerle">KEŞFET <span>↓</span></a></section>
<div class="expertise-strip"><div class="container"><span>ELEKTRİK MÜHENDİSLİĞİ</span><i>✦</i><span>ENDÜSTRİYEL OTOMASYON</span><i>✦</i><span>PANO & TESİSAT</span><i>✦</i><span>BAKIM & SERVİS</span></div></div>
<section class="about section" id="hakkimizda" aria-labelledby="about-title"><div class="container about-layout"><div class="experience"><span class="eyebrow">DÜNDEN BUGÜNE YAYBOZ</span><strong>30<span>yıllık</span></strong><p>tecrübe, aynı titizlik.</p><div class="experience-line"></div><span class="location-label">ÜMRANİYE · İSTANBUL</span></div><div class="about-copy"><p class="eyebrow">HAKKIMIZDA</p><h2 id="about-title">İşin başından sonuna,<br><span>yanınızdayız.</span></h2><p>Yayboz Elektrik olarak elektrik ve elektronik mühendisliği, proje, taahhüt ve otomasyon alanlarında hizmet veriyoruz. Mühendis kadromuz ve 30 yıllık tecrübemizle, sanayi bölgelerinden fabrikalara, iş yerlerinden konutlara kadar elektrik işlerinizi üstleniyoruz.</p><p>Projelendirme, malzeme tedariği, pano montajı ve tesisat uygulamasını; arıza teşhis, bakım, onarım ve servis hizmetleriyle tamamlıyoruz.</p><div class="about-points"><span>{icon('check')} Mühendis kadrosu</span><span>{icon('check')} İhtiyaca özel uygulama</span><span>{icon('check')} Proje ve saha tecrübesi</span><span>{icon('check')} Bakım ve teknik destek</span></div><a class="text-link" href="#iletisim">Tanışalım, projenizi konuşalım {icon('arrow')}</a></div></div></section>
<section class="services section" id="hizmetler" aria-labelledby="services-title"><div class="container"><div class="section-heading"><div><p class="eyebrow">NELER YAPIYORUZ?</p><h2 id="services-title">Elektriğin olduğu<br><span>her yerde çözüm.</span></h2></div><p>Bir makineden bir üretim tesisine kadar.<br>Mühendislik, uygulama ve servis aynı çatı altında.</p></div><div class="services-grid">{service_html}</div><div class="service-footer"><span>İşinize uygun çözümü birlikte belirleyelim.</span><a href="tel:+902164990983" class="text-link">0216 499 09 83 {icon('arrow')}</a></div></div></section>
<section class="featured section" id="uygulamalar" aria-labelledby="featured-title"><div class="container"><div class="section-heading"><div><p class="eyebrow">UYGULAMALARIMIZDAN</p><h2 id="featured-title">Tecrübe, <span>sahada görünür.</span></h2></div><a class="text-link" href="#projeler">Tüm proje listesi {icon('arrow')}</a></div><p class="section-intro">Makine otomasyonu, kontrol panoları ve operatör arayüzlerinden örnekler. Görselleri açarak proje ayrıntılarını inceleyin.</p><div class="featured-grid">{featured_html}</div><p class="source-note">Bu bölümdeki fotoğraflar ve teknik ekranlar kendi proje sunumumuzdan alınmıştır.</p></div></section>
<section class="contact section" id="iletisim" aria-labelledby="contact-title"><div class="container contact-layout"><div class="contact-info"><p class="eyebrow light">İLETİŞİM</p><h2 id="contact-title">Bir ihtiyacınız var.<br><span>Birlikte çözelim.</span></h2><p>Proje, taahhüt, malzeme tedariği veya teknik servis.<br>İhtiyacınızı bize anlatın, birlikte değerlendirelim.</p><a class="main-phone" href="tel:+902164990983">0216 499 09 83 {icon('up')}</a><div class="contact-mobiles"><a href="tel:+905359685560">0535 968 55 60</a><a href="tel:+905333268092">0533 326 80 92</a></div><p class="people">Yücel Bozkurt & Durmuş Yayla</p><div class="address-block">{icon('pin')}<div><address>4. Esenşehir Mahallesi, Atılım Sokak No:42/2<br>Yukarı Dudullu, Ümraniye / İstanbul</address><a href="https://www.google.com/maps/search/?api=1&query=Yayboz%20Elektrik%20At%C4%B1l%C4%B1m%20Sokak%2042%2F2%20Esen%C5%9Fehir%20%C3%9Cmraniye%20%C4%B0stanbul" target="_blank" rel="noopener noreferrer">Haritada yol tarifi al {icon('up')}</a></div></div><small class="fax">Faks: 0216 499 09 82</small></div><form class="contact-form" id="contact-form"><span class="eyebrow">HIZLICA İLETİŞİME GEÇİN</span><h3>Projenizden bahsedin.</h3><p>Bilgileri doldurun, mesajınızı WhatsApp üzerinden bize iletin.</p><label for="contact-name">Adınız / Firmanız <span>*</span></label><input id="contact-name" name="name" autocomplete="organization" placeholder="Adınız veya firma adınız" maxlength="100" required><label for="contact-service">İlgilendiğiniz hizmet</label><select id="contact-service" name="service"><option>Elektrik mühendisliği, proje ve taahhüt</option><option>Otomasyon sistemleri</option><option>Pano imalatı ve montajı</option><option>Sanayi ve fabrika tesisatları</option><option>Konut ve iş yeri tesisatları</option><option>Arıza teşhis, bakım ve servis</option><option>Malzeme alım satımı</option><option>Tadilat ve revizyon</option><option>Elektrik proje çizimi</option><option>Diğer elektrik işleri</option></select><label for="contact-message">Nasıl yardımcı olabiliriz? <span>*</span></label><textarea id="contact-message" name="message" rows="3" placeholder="İhtiyacınızı kısaca yazın…" maxlength="1500" required></textarea><button class="button" type="submit">WhatsApp'ta devam et {icon('message')}</button><p class="form-note">Mesajınız WhatsApp açıldıktan sonra sizin onayınızla gönderilir. Bu formdaki bilgiler sitede kaydedilmez.</p><noscript><p>Bu form için JavaScript gereklidir. <a href="https://wa.me/905359685560" target="_blank" rel="noopener noreferrer">WhatsApp üzerinden doğrudan ulaşın.</a></p></noscript></form></div></section>
<section class="catalog section" id="projeler" aria-labelledby="catalog-title"><div class="container"><div class="section-heading"><div><p class="eyebrow">PROJE PORTFÖYÜ</p><h2 id="catalog-title">Otomasyon projeleri<span class="orange-dot">.</span></h2></div><p>Kontrol sistemlerinden elektrik devre çizimlerine,<br>birikimimizi yansıtan çalışmalarımız.</p></div><div class="catalog-controls"><div class="filters" role="group" aria-label="Proje kategorisi"><button type="button" class="filter active" data-filter="all" aria-pressed="true">Tüm projeler <span>{len(projects)}</span></button><button type="button" class="filter" data-filter="{auto}" aria-pressed="false">Otomasyon</button><button type="button" class="filter" data-filter="{siemens}" aria-pressed="false">Siemens / WinCC</button><button type="button" class="filter" data-filter="{drawing}" aria-pressed="false">Proje çizimleri</button></div><label class="search-field">{icon('search')}<input type="search" id="project-search" placeholder="Proje ara…" aria-label="Projelerde ara" autocomplete="off"></label></div><p id="result-count" class="result-count" role="status" aria-live="polite">{len(projects)} proje listeleniyor</p><div class="catalog-columns">{catalog}</div><div class="empty-state" id="empty-state" hidden><h3>Bu aramayla eşleşen proje bulunamadı.</h3><p>Başka bir kelime deneyin veya tüm projeleri görüntüleyin.</p><button type="button" class="button" id="reset-search">Tüm projeleri göster {icon('arrow')}</button></div><p class="catalog-note">“Görseller” bağlantılı projelerde özgün sunum sayfalarını inceleyebilirsiniz. Simülasyon ve eğitim çalışmaları ayrıca belirtilmiştir.</p></div></section></main>
<footer class="site-footer"><div class="container footer-top"><a href="#ana-sayfa" class="brand" aria-label="Yayboz Elektrik ana sayfa">{logo()}</a><p>Mühendislikten uygulamaya.<br>30 yıllık tecrübeyle.</p><a class="text-link" href="#ana-sayfa">Başa dön ↑</a></div><div class="container footer-bottom"><span>© 2026 Yayboz Elektrik. Tüm hakları saklıdır.</span><span>Elektrik · Elektronik · Otomasyon · Proje · Taahhüt</span><a href="gizlilik.html">Gizlilik</a></div></footer>
<a class="floating-contact" href="https://wa.me/905359685560?text=Merhaba%2C%20Yayboz%20Elektrik%20hizmetleriniz%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" aria-label="Yayboz Elektrik ile WhatsApp üzerinden iletişime geçin">{icon('message')}<span>Birlikte çözelim</span></a>
<dialog id="project-dialog" aria-labelledby="dialog-title"><div class="dialog-header"><div><span class="eyebrow" id="dialog-category"></span><h2 id="dialog-title"></h2></div><button type="button" class="icon-button dialog-close" aria-label="Proje penceresini kapat">{icon('close')}</button></div><div class="dialog-body"><p id="dialog-description"></p><div class="slide-stage"><img id="dialog-image" src="assets/proje-08.webp" alt="" width="1920" height="1080"></div><div class="slide-controls"><button type="button" class="slide-prev" aria-label="Önceki görsel">← Önceki</button><span id="slide-count" aria-live="polite"></span><button type="button" class="slide-next" aria-label="Sonraki görsel">Sonraki →</button></div><p class="source-note"><a id="full-image-link" class="text-link" href="assets/proje-08.webp" target="_blank" rel="noopener noreferrer">Görseli tam boy aç ↗</a></p><p class="source-note">Özgün proje sunumundan. Teknik bilgiler sunumun hazırlandığı projeye aittir.</p></div></dialog>
</body></html>'''
(DIST/'index.html').write_text(html)
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+BASE+'</loc></url></urlset>')
privacy='''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gizlilik · Yayboz Elektrik</title><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="styles.css"></head><body><main class="container privacy"><a href="./" class="text-link">← Yayboz Elektrik ana sayfa</a><p class="eyebrow">GİZLİLİK</p><h1>Sitenin veri kullanımı</h1><p>Bu tanıtım sitesinde kullanıcı hesabı, analitik izleme veya reklam çerezi bulunmaz. İletişim formuna yazdığınız bilgiler siteye kaydedilmez; WhatsApp bağlantısını oluşturmak için tarayıcınızda kullanılır.</p><h2>İletişim bağlantıları</h2><p>WhatsApp bağlantısını açtığınızda adınız/firma adınız, seçtiğiniz hizmet ve yazdığınız mesaj WhatsApp'a aktarılır. Gönderme işlemini WhatsApp üzerinden siz tamamlarsınız. WhatsApp ve Google Haritalar açıldığında ilgili hizmetin kendi veri kullanım koşulları geçerlidir.</p><h2>Barındırma</h2><p>Sayfalarımız barındırma sağlayıcısı üzerinden sunulur. Sağlayıcı, bağlantının kurulması ve güvenliği için IP adresi ve teknik istek bilgilerini işleyebilir.</p><h2>Bize ulaşın</h2><p>Yayboz Elektrik · 4. Esenşehir Mahallesi, Atılım Sokak No:42/2, Yukarı Dudullu, Ümraniye / İstanbul</p><p><a href="tel:+902164990983">0216 499 09 83</a></p></main></body></html>'''
(DIST/'gizlilik.html').write_text(privacy)
print(f'Built {len(projects)} projects, {len(services)} services, main page and privacy page.')
