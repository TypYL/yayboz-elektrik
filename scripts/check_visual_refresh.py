"""Browser acceptance for photography, control-circuit interaction and accessibility."""
import json, os, threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'
OUT.mkdir(exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=None
BASE=os.environ.get('YAYBOZ_QA_URL')
if not BASE:
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT/'dist')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 BASE=f'http://127.0.0.1:{server.server_address[1]}/'
label='live' if BASE.startswith('https:') else 'local'
report={'base':BASE,'checks':[],'errors':[],'accessibility':[]}
def check(name,condition):
 report['checks'].append({'name':name,'passed':bool(condition)})
 if not condition: raise AssertionError(name)
def pause_auto(page):
 button=page.locator('#circuit-auto')
 if button.get_attribute('aria-pressed')=='true': button.click()

try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--disable-gpu'])
  page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
  page.on('pageerror',lambda err:report['errors'].append(str(err)))
  page.goto(BASE,wait_until='networkidle')
  page.evaluate('document.fonts.ready')
  check('six featured project cards',page.locator('.project-card').count()==6)
  check('four reconstructed images clearly labelled',page.locator('.image-origin').count()==4)
  check('navy brand palette',page.locator('html').evaluate('el=>getComputedStyle(el).getPropertyValue("--deep").trim()')=='#071c36')
  page.screenshot(path=str(OUT/f'{label}-v2-desktop-hero.png'))
  for name in ['hakkimizda','uygulamalar']:
   target=page.locator('#'+name)
   target.scroll_into_view_if_needed()
   page.wait_for_timeout(350)
   page.locator('#'+name+' img').evaluate_all('(images)=>Promise.all(images.map(i=>i.decode()))')
   target.screenshot(path=str(OUT/f'{label}-v2-desktop-{name}.png'),style='.site-header,.floating-contact,.skip-link{visibility:hidden!important}')
  circuit=page.locator('#control-circuit')
  circuit.scroll_into_view_if_needed()
  page.wait_for_timeout(300)
  pause_auto(page)
  check('pause stops all animation',circuit.get_attribute('data-motion')=='off')
  page.locator('#circuit-start').click()
  check('manual start energises circuit',circuit.get_attribute('data-phase')=='start')
  page.wait_for_timeout(1700)
  check('holding contact keeps motor running',circuit.get_attribute('data-phase')=='hold')
  rotor=page.locator('.motor-rotor')
  first=rotor.evaluate('el=>getComputedStyle(el).transform')
  page.wait_for_timeout(220)
  check('motor visibly rotates',rotor.evaluate('el=>getComputedStyle(el).transform')!=first)
  page.locator('#otomasyon').screenshot(path=str(OUT/f'{label}-v2-desktop-running.png'))
  page.locator('#circuit-stop').click()
  check('stop opens circuit',circuit.get_attribute('data-phase')=='stop')
  first=rotor.evaluate('el=>getComputedStyle(el).transform')
  page.wait_for_timeout(250)
  check('stop halts rotor',rotor.evaluate('el=>getComputedStyle(el).transform')==first)
  page.locator('#otomasyon').screenshot(path=str(OUT/f'{label}-v2-desktop-stopped.png'))
  page.locator('#circuit-start').focus()
  page.keyboard.press('Enter')
  check('start keyboard accessible',circuit.get_attribute('data-phase')=='start')
  page.evaluate('scrollTo({top:0,behavior:"instant"})')
  page.wait_for_timeout(350)
  check('offscreen animation suspended',circuit.get_attribute('data-motion')=='off')
  circuit.scroll_into_view_if_needed()
  page.wait_for_timeout(350)
  check('onscreen manual animation resumes',circuit.get_attribute('data-motion')=='on')
  page.locator('#circuit-auto').click()
  check('automatic cycle enabled',page.locator('#circuit-auto').get_attribute('aria-pressed')=='true')
  page.wait_for_function('document.querySelector("#control-circuit").dataset.phase==="stop"',timeout=9000)
  check('automatic demonstration reaches stop',circuit.get_attribute('data-phase')=='stop')
  pause_auto(page)
  for width in [320,390,768,1024,1920]:
   page.set_viewport_size({'width':width,'height':900})
   check(f'no overflow at {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   if width==390:
    page.locator('#circuit-start').click()
    page.wait_for_timeout(1600)
    page.locator('#otomasyon').screenshot(path=str(OUT/f'{label}-v2-mobile-automation.png'),style='.site-header,.floating-contact,.skip-link{visibility:hidden!important}')
    for name in ['ana-sayfa','hakkimizda','uygulamalar']:
     page.locator('#'+name).screenshot(path=str(OUT/f'{label}-v2-mobile-{name}.png'),style='.site-header,.floating-contact,.skip-link{visibility:hidden!important}')
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000})
   page.add_script_tag(path=str(ROOT/'.tools/qa/node_modules/axe-core/axe.min.js'))
   violations=page.evaluate('async()=> (await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})).violations')
   report['accessibility'].append({'width':width,'violations':violations})
   check(f'WCAG A/AA axe scan at {width}',not violations)
  page.emulate_media(reduced_motion='reduce')
  circuit.scroll_into_view_if_needed()
  page.locator('#circuit-start').click()
  check('reduced motion shows static running state',circuit.get_attribute('data-phase')=='hold' and circuit.get_attribute('data-motion')=='off')
  check('reduced motion disables autoplay',page.locator('#circuit-auto').is_disabled())
  check('reduced motion removes rotor animation',rotor.evaluate('el=>getComputedStyle(el).animationName')=='none')
  page.locator('#circuit-stop').click()
  check('reduced motion still allows stop',circuit.get_attribute('data-phase')=='stop')
  check('no browser errors',not report['errors'])
  browser.close()
finally:
 if server: server.shutdown()
 (OUT/f'{label}-visual-refresh-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({'base':BASE,'passed':sum(c['passed'] for c in report['checks']),'checks':len(report['checks']),'errors':report['errors'],'accessibility_violations':[len(v['violations']) for v in report['accessibility']]},ensure_ascii=False))
