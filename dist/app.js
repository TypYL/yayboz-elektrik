'use strict';

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
function closeMenu() {
  navigation.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Menüyü aç');
}
menuButton.addEventListener('click', () => {
  const open = navigation.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
});
navigation.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
window.matchMedia('(min-width: 701px)').addEventListener('change', e => { if (e.matches) closeMenu(); });

const sections = document.querySelectorAll('main section[id]');
const sectionObserver = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    navigation.querySelectorAll('a:not(.button)').forEach(a => {
      const current = a.hash === '#' + entry.target.id;
      a.classList.toggle('active', current);
      if (current) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
  }
}, { rootMargin: '-15% 0px -60% 0px', threshold: 0 });
sections.forEach(section => sectionObserver.observe(section));

const filters = [...document.querySelectorAll('.filter')];
const search = document.querySelector('#project-search');
const catalogItems = [...document.querySelectorAll('.catalog-item')];
const catalogGroups = [...document.querySelectorAll('.catalog-group')];
let activeFilter = 'all';
const normalize = text => text.toLocaleLowerCase('tr-TR').replaceAll('ı', 'i').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
function filterProjects() {
  const term = normalize(search.value.trim());
  let count = 0;
  catalogItems.forEach(item => {
    const visible = (activeFilter === 'all' || activeFilter === item.dataset.category) && normalize(item.dataset.title).includes(term);
    item.hidden = !visible;
    if (visible) count++;
  });
  catalogGroups.forEach(group => { group.hidden = !group.querySelector('.catalog-item:not([hidden])'); });
  document.querySelector('#result-count').textContent = `${count} proje listeleniyor`;
  document.querySelector('#empty-state').hidden = count !== 0;
  document.querySelector('.catalog-columns').classList.toggle('filtered', activeFilter !== 'all');
  filters.forEach(button => {
    const active = button.dataset.filter === activeFilter;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
}
filters.forEach(button => button.addEventListener('click', () => { activeFilter = button.dataset.filter; filterProjects(); }));
search.addEventListener('input', filterProjects);
document.querySelector('#reset-search').addEventListener('click', () => { activeFilter = 'all'; search.value = ''; filterProjects(); search.focus(); });

document.querySelector('#contact-form').addEventListener('submit', e => {
  e.preventDefault();
  const form = e.currentTarget;
  const nameInput = form.elements.name;
  const messageInput = form.elements.message;
  nameInput.setCustomValidity(nameInput.value.trim() ? '' : 'Lütfen adınızı veya firma adınızı yazın.');
  messageInput.setCustomValidity(messageInput.value.trim() ? '' : 'Lütfen ihtiyacınızı kısaca yazın.');
  if (!form.reportValidity()) return;
  const message = `Merhaba Yayboz Elektrik,\n\nAd / Firma: ${nameInput.value.trim()}\nHizmet: ${form.elements.service.value}\n\n${messageInput.value.trim()}`;
  const link = document.createElement('a');
  link.href = `https://wa.me/905359685560?text=${encodeURIComponent(message)}`;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  document.body.appendChild(link);
  link.click();
  link.remove();
});
document.querySelectorAll('#contact-name, #contact-message').forEach(input => input.addEventListener('input', () => input.setCustomValidity('')));

const dialog = document.querySelector('#project-dialog');
const dialogImage = document.querySelector('#dialog-image');
let projectsPromise;
let selectedProject;
let slideIndex = 0;
let returnFocus;
function renderSlide() {
  const num = String(selectedProject.slides[slideIndex]).padStart(2, '0');
  dialogImage.src = `assets/proje-${num}.webp`;
  document.querySelector("#full-image-link").href = dialogImage.src;
  dialogImage.alt = `${selectedProject.title} — özgün proje sunumu, görsel ${slideIndex + 1}`;
  document.querySelector('#slide-count').textContent = `${slideIndex + 1} / ${selectedProject.slides.length}`;
  document.querySelector('.slide-prev').disabled = slideIndex === 0;
  document.querySelector('.slide-next').disabled = slideIndex === selectedProject.slides.length - 1;
}
document.querySelectorAll('[data-project]').forEach(button => button.addEventListener('click', async () => {
  returnFocus = button;
  try {
    projectsPromise ||= fetch('assets/projects.json').then(response => { if (!response.ok) throw new Error('Project content unavailable'); return response.json(); });
    const projects = await projectsPromise;
    selectedProject = projects.find(p => p.id === button.dataset.project);
    if (!selectedProject || !selectedProject.slides.length) return;
    slideIndex = 0;
    document.querySelector('#dialog-category').textContent = selectedProject.category + (selectedProject.note ? ` · ${selectedProject.note}` : '');
    document.querySelector('#dialog-title').textContent = selectedProject.title;
    document.querySelector('#dialog-description').textContent = selectedProject.description || 'Çalışmanın teknik ayrıntılarını özgün proje sunumu görsellerinde inceleyebilirsiniz.';
    renderSlide();
    dialog.showModal();
    document.body.classList.add('modal-open');
  } catch {
    projectsPromise = undefined;
    document.querySelector('#dialog-category').textContent = 'PROJE GÖRSELLERİ';
    document.querySelector('#dialog-title').textContent = 'Görseller şu anda yüklenemedi.';
    document.querySelector('#dialog-description').textContent = 'İnternet bağlantınızı kontrol edip tekrar deneyin. Proje hakkında bilgi almak için 0216 499 09 83 numarasından bize ulaşabilirsiniz.';
    document.querySelector('.slide-stage').hidden = true;
    document.querySelector('.slide-controls').hidden = true;
    dialog.showModal();
    document.body.classList.add('modal-open');
  }
}));
dialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  document.querySelector('.slide-stage').hidden = false;
  document.querySelector('.slide-controls').hidden = false;
  returnFocus?.focus({ preventScroll: true });
});
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', e => { if (e.target === dialog) { const rect = dialog.getBoundingClientRect(); if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) dialog.close(); } });
document.querySelector('.slide-prev').addEventListener('click', () => { if (slideIndex > 0) { slideIndex--; renderSlide(); } });
document.querySelector('.slide-next').addEventListener('click', () => { if (slideIndex < selectedProject.slides.length - 1) { slideIndex++; renderSlide(); } });
dialog.addEventListener('keydown', e => {
  if (!selectedProject) return;
  if (e.key === 'ArrowLeft' && slideIndex > 0) { e.preventDefault(); slideIndex--; renderSlide(); }
  if (e.key === 'ArrowRight' && slideIndex < selectedProject.slides.length - 1) { e.preventDefault(); slideIndex++; renderSlide(); }
});
