import json, re, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'
OUT.mkdir(exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self, *args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT/'dist')))
threading.Thread(target=server.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{server.server_address[1]}/'
report={'checks':[],'errors':[]}
def check(name, condition):
 report['checks'].append({'name':name,'passed':bool(condition)})
 if not condition: raise AssertionError(name)

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--disable-gpu'])
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 page.on('pageerror',lambda err:report['errors'].append(str(err)))
 page.on('console',lambda msg:report['errors'].append(msg.text) if msg.type=='error' else None)
 response=page.goto(BASE,wait_until='networkidle')
 check('homepage HTTP 200',response.status==200)
 page.evaluate('document.fonts.ready')
 check('34 projects included',page.locator('.catalog-item').count()==34)
 check('9 service categories included',page.locator('.service').count()==9)
 check('engineering team and 30 years present',page.get_by_text('Mühendis kadrosu',exact=True).count()>0 and page.locator('.experience').inner_text().find('30')>=0)
 check('desktop no horizontal overflow',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
 page.screenshot(path=str(OUT/'desktop-hero.png'))
 page.screenshot(path=str(OUT/'desktop-full.png'),full_page=True)
 page.locator('#project-search').fill('kumlama')
 check('Turkish search matches both blasting projects',page.locator('.catalog-item:visible').count()==2)
 page.locator('#project-search').fill('olcum')
 check('accent insensitive search',page.locator('.catalog-item:visible').count()==1)
 page.locator('#project-search').fill('zzzzzzzz')
 check('empty state',page.locator('#empty-state').is_visible())
 page.locator('#reset-search').click()
 check('reset restores all projects',page.locator('.catalog-item:visible').count()==34)
 page.get_by_role('button',name='Siemens / WinCC',exact=True).click()
 check('Siemens filter',page.locator('.catalog-item:visible').count()==5)
 check('simulation disclosure',page.locator('.catalog-item:visible .tag').all_text_contents()==['Simülasyon','Simülasyon','Simülasyon'])
 page.get_by_role('button',name='Proje çizimleri',exact=True).click()
 check('drawing filter',page.locator('.catalog-item:visible').count()==11)
 page.get_by_role('button',name=re.compile('Tüm projeler 34')).click()
 page.locator('.project-card[data-project="p07"]').click()
 page.locator('#project-dialog').wait_for(state='visible',timeout=5000)
 check('project modal opens',page.locator('#project-dialog').is_visible())
 check('gallery count',page.locator('#slide-count').inner_text()=='1 / 7')
 page.locator('.slide-next').click()
 check('gallery advances',page.locator('#slide-count').inner_text()=='2 / 7')
 page.screenshot(path=str(OUT/'desktop-project-modal.png'))
 page.keyboard.press('Escape')
 check('modal Escape closes',not page.locator('#project-dialog').is_visible())
 check('focus restored to project',page.locator('.project-card[data-project="p07"]').evaluate('(el)=>el===document.activeElement'))
 page.evaluate("""document.addEventListener('click',e=>{const a=e.target.closest('a');if(a?.href.startsWith('https://wa.me/')){e.preventDefault();window.__contactUrl=a.href}},true)""")
 page.locator('#contact-form button').click()
 check('empty form cannot submit',page.evaluate('window.__contactUrl===undefined'))
 page.locator('#contact-name').fill('Örnek Firma')
 page.locator('#contact-service').select_option(label='Pano imalatı ve montajı')
 page.locator('#contact-message').fill('Dağıtım panosu için görüşmek istiyorum.')
 page.locator('#contact-form button').click()
 url=page.evaluate('window.__contactUrl')
 from urllib.parse import urlparse,parse_qs
 message=parse_qs(urlparse(url).query)['text'][0]
 check('WhatsApp uses supplied number and user text',urlparse(url).path=='/905359685560' and 'Örnek Firma' in message and 'Pano imalatı' in message)
 check('phone links match business card',set(page.locator('a[href^="tel:"]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))'))=={'tel:+902164990983','tel:+905359685560','tel:+905333268092'})
 for width in [320,390,768,1024,1920]:
  page.set_viewport_size({'width':width,'height':844 if width<700 else 1000})
  page.goto(BASE,wait_until='networkidle')
  check(f'no horizontal overflow at {width}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  if width==390:
   page.screenshot(path=str(OUT/'mobile-hero.png'))
   page.screenshot(path=str(OUT/'mobile-full.png'),full_page=True)
   page.locator('.menu-toggle').click()
   check('mobile navigation opens',page.locator('#main-nav').is_visible())
   page.locator('#main-nav a[href="#hizmetler"]').click()
   check('mobile navigation closes after selection',page.locator('.menu-toggle').get_attribute('aria-expanded')=='false')
   page.locator('.project-card[data-project="p07"]').click()
   page.screenshot(path=str(OUT/'mobile-project-modal.png'))
   check('mobile modal fits viewport',page.locator('#project-dialog').bounding_box()['width']<=390)
   page.locator('.dialog-close').click()
   page.locator('#iletisim').screenshot(path=str(OUT/'mobile-contact.png'))
  broken=page.locator('img').evaluate_all('(imgs)=>imgs.filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src)')
  check(f'no broken images at {width}px',len(broken)==0)
 check('no browser errors',not report['errors'])
 page.goto(BASE+'gizlilik.html',wait_until='networkidle')
 check('privacy page',page.get_by_role('heading',name='Sitenin veri kullanımı').is_visible())
 browser.close()
server.shutdown()
(OUT/'browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
