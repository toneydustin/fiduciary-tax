
const BRAND_SVG = `<svg class="nav-logo-mark" viewBox="0 0 244.4 252.33" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M114.94,53.52l-2,16.72h-.56c-2.16-10.48-8.24-15.68-17.92-15.68h-.88l-4.24,27.28h.88c5.12,0,10.4-4.4,12.96-11.28h.64l-3.76,23.68h-.64c-.48-8.64-5.76-11.36-9.84-11.36h-.48l-4.56,25.68h5.92l-.24.96h-26.4l.08-.96h4.16l8.88-54h-4.48l.24-1.04h42.24Z"/><path d="M188.61,72.84h-.72c-1.44-9.6-5.68-18.88-13.68-19.28l-9.12,54h7.52l-.16.96h-31.12l.24-.96h6.96l9.12-54c-8,1.36-15.84,8.88-19.92,19.28h-.8l3.44-20.32h51.52l-3.28,20.32Z"/><path d="M141.79,125.86c-.64,13.2-7.76,24.72-28.64,24.72-15.76,0-24.88-5.44-24.88-15.76,0-9.76,11.04-15.12,24.64-15.92v-.4c-10.72-.08-18.4-4.16-18.4-10.88,0-10,10.32-14.8,25.12-14.8,7.6,0,16.48,2.08,16.48,10.4,0,6.88-4.4,9.04-8.08,9.04-4.8,0-6.48-3.2-6.48-6.16,0-1.52.48-2.96,1.12-4h4.4c.8-1.52,1.2-2.88,1.2-4,0-2.8-2.32-4.08-5.28-4.08-4.24,0-9.68,3.36-9.68,14.48,0,2.8.4,7.76,2,9.92,2-1.04,3.84-1.76,5.44-1.76,1.04,0,2.72.56,2.72,2.24,0,2-1.28,2.72-2.96,2.72-2.08,0-4.32-1.52-5.68-2.48-3.68,3.44-6.24,6.56-6.24,16.72,0,5.44,2.96,11.84,12.4,11.84,11.84,0,19.28-10.72,19.28-21.68l-12.16,1.52c-2.4.32-2.56,1.12-3.04,3.52l-.64-.08c.32-11.76,3.04-16.48,8.16-17.52,2.88-.4,16.08-1.92,19.44-2.64,1.44-.32,2.16-.96,2.48-3.6l.64.08c.4,8.32-1.36,16.4-7.36,17.44l-6,1.12Z"/><path d="M76.14,177.68h-14.72l-8.88,18.08h5.76l-.16.96h-10.48l.16-.96h3.28l27.52-55.52h7.84l11.92,55.52h3.04l-.16.96h-27.04l.16-.96h5.28l-3.52-18.08ZM61.9,176.48h14l-3.68-20.64-10.32,20.64Z"/><path d="M156.27,186.08c0-6.88-5.44-8.16-13.76-11.28-3.2-1.28-11.12-4.64-11.12-15.84,0-12.96,10.8-19.12,20.56-19.12,7.76,0,12.4,3.36,13.84,3.36,1.04,0,1.92-1.12,2.64-2.64h.64l-2.64,17.44h-.56c-2.32-7.36-6.24-17.28-14.08-17.28-6,0-9.04,3.92-9.04,8.88,0,6.16,4.48,8,8.16,9.6,6.56,2.72,16.56,5.52,16.56,17.44,0,13.28-10.4,20.88-21.68,20.88-8.16,0-14.72-3.52-16.56-3.52-1.04,0-1.6.8-2.72,3.52h-.88l3.12-19.44h.64c1.2,6.32,5.84,18.48,16.32,18.48,6.8,0,10.56-4.16,10.56-10.48Z"/></svg>`;

function getP() {
  const path = window.location.pathname;
  if (path.includes('/services/')) return '../';
  if (path.includes('/blog/')) return '../';
  return '';
}

function buildNav() {
  const p = getP();
  return `<nav>
  <a href="${p}index.html" class="nav-logo">${BRAND_SVG}<span class="nav-logo-text"><span class="nav-logo-name">Fiduciary Tax &amp; Accounting Services</span><span class="nav-logo-sub">Estate &middot; Trust &middot; Fiduciary Tax</span></span></a>
  <ul class="nav-links" id="navLinks">
    <li><a href="${p}professional-fiduciaries.html">Professional Fiduciaries</a></li>
    <li><a href="${p}personal-fiduciaries.html">Personal Fiduciaries</a></li>
    <li><a href="${p}individual.html">Individual</a></li>
    <li><a href="${p}blog/index.html">News &amp; Insights</a></li>
    <li><a href="${p}index.html#contact">Contact</a></li>
    <li><a href="https://portal.fiduciary.tax" target="_blank" rel="noopener" class="nav-portal">Client Portal</a></li>
  </ul>
  <button class="nav-hamburger" onclick="toggleNav()" aria-label="Menu"><span></span><span></span><span></span></button>
</nav><div class="divider-gold"></div>`;
}

function buildFooter() {
  const p = getP();
  return `<footer><div class="foot-inner">
  <a href="${p}index.html" class="foot-logo">${BRAND_SVG}<span class="foot-logo-name">Fiduciary Tax &amp; Accounting Services</span></a>
  <div class="foot-legal">&copy; 2026 Fiduciary Tax &amp; Accounting Services, LLC &middot; fiduciary.tax &middot; All rights reserved<br>d/b/a Fiduciary Tax &amp; Accounting Services &middot; Birmingham, AL</div>
</div></footer>`;
}

function toggleNav() { document.getElementById('navLinks').classList.toggle('open'); }

function switchService(audienceId, which, btn) {
  const panel = document.getElementById('audience-' + audienceId);
  panel.querySelectorAll('.service-tab-btn').forEach(b => b.classList.remove('active'));
  panel.querySelectorAll('.service-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(audienceId + '-' + which).classList.add('active');
}

function goToCategory(audienceId, which) {
  const panel = document.getElementById('audience-' + audienceId);
  const btn = panel.querySelector('.service-tab-btn[data-service="' + which + '"]');
  if (!btn) return;
  switchService(audienceId, which, btn);
  panel.querySelector('.service-tabs').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function handleSubmit() {
  const name = document.getElementById('f-name').value.trim();
  const email = document.getElementById('f-email').value.trim();
  const who = document.getElementById('f-who') ? document.getElementById('f-who').value : '';
  const phone = document.getElementById('f-phone') ? document.getElementById('f-phone').value.trim() : '';
  const msg = document.getElementById('f-msg') ? document.getElementById('f-msg').value.trim() : '';
  if (!name || !email) { alert('Please enter your name and email.'); return; }
  const btn = document.querySelector('.fsub');
  btn.disabled = true; btn.style.opacity = '0.5'; btn.textContent = 'Sending...';
  try {
    const res = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        access_key: 'b7e6280a-0000-4b71-ab62-39eeb9ebd5b3',
        subject: 'New Contact Form Submission — fiduciary.tax',
        from_name: 'FTAS Website',
        name: name,
        email: email,
        phone: phone || 'Not provided',
        'I am a': who || 'Not selected',
        message: msg || 'No message provided'
      })
    });
    const data = await res.json();
    if (data.success) {
      document.getElementById('confirm-msg').style.display = 'block';
      btn.textContent = 'Sent';
    } else {
      btn.disabled = false; btn.style.opacity = '1'; btn.textContent = 'Send Message';
      alert('Something went wrong. Please email info@fiduciary.tax directly.');
    }
  } catch(e) {
    btn.disabled = false; btn.style.opacity = '1'; btn.textContent = 'Send Message';
    alert('Something went wrong. Please email info@fiduciary.tax directly.');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.body.insertAdjacentHTML('afterbegin', buildNav());
  document.body.insertAdjacentHTML('beforeend', buildFooter());
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth' }); }
    });
  });
});
