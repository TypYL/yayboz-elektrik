(() => {
  'use strict';
  const panel = document.getElementById('control-circuit');
  if (!panel) return;
  const start = document.getElementById('circuit-start');
  const stop = document.getElementById('circuit-stop');
  const toggle = document.getElementById('circuit-auto');
  const title = document.getElementById('circuit-state-title');
  const description = document.getElementById('circuit-state-description');
  const announcement = document.getElementById('circuit-announcement');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const states = {
    idle: ['Sistem hazır', 'Başlatma sinyali bekleniyor.'],
    start: ['Başlatma sinyali', 'Kontaktör çekiyor, motor devreye giriyor.'],
    hold: ['Motor çalışıyor', 'Yardımcı kontak devreyi tutuyor.'],
    stop: ['Motor durdu', 'Durdur kontağı açıldı, enerji akışı kesildi.']
  };
  const next = {idle: 'start', start: 'hold', hold: 'stop', stop: 'idle'};
  const duration = {idle: 1400, start: 1500, hold: 4500, stop: 1800};
  let phase = 'idle';
  let automatic = !reduced.matches;
  let paused = false;
  let inView = false;
  let timer;

  function paint(announce = false) {
    panel.dataset.phase = phase;
    panel.dataset.motion = inView && !document.hidden && !reduced.matches && !paused ? 'on' : 'off';
    title.textContent = states[phase][0];
    description.textContent = states[phase][1];
    toggle.setAttribute('aria-pressed', String(automatic));
    toggle.setAttribute('aria-label', reduced.matches ? 'Hareket azaltma tercihi etkin' : automatic ? 'Otomatik animasyonu duraklat' : 'Otomatik animasyonu başlat');
    toggle.textContent = automatic ? 'Ⅱ' : '↻';
    toggle.disabled = reduced.matches;
    if (announce) announcement.textContent = states[phase].join('. ');
  }

  function schedule() {
    clearTimeout(timer);
    paint();
    if (!inView || document.hidden || paused) return;
    // Manual start still releases the start button into the holding contact.
    if (!automatic && phase !== 'start') return;
    timer = setTimeout(() => {
      phase = automatic ? next[phase] : 'hold';
      schedule();
    }, reduced.matches ? 0 : duration[phase]);
  }

  start.addEventListener('click', () => {
    automatic = false;
    paused = false;
    phase = reduced.matches ? 'hold' : 'start';
    schedule();
    paint(true);
  });
  stop.addEventListener('click', () => {
    automatic = false;
    paused = false;
    phase = 'stop';
    schedule();
    paint(true);
  });
  toggle.addEventListener('click', () => {
    if (reduced.matches) return;
    automatic = !automatic;
    paused = !automatic;
    schedule();
    announcement.textContent = automatic ? 'Otomatik animasyon başladı.' : 'Animasyon duraklatıldı.';
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches) {
      automatic = false;
      paused = false;
      if (phase === 'start') phase = 'hold';
    }
    schedule();
  });
  document.addEventListener('visibilitychange', schedule);
  new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    schedule();
  }, {threshold: .2}).observe(panel);
  paint();
})();
