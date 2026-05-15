// ── Star rating input ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  const stars     = document.querySelectorAll('.star-btn');
  const ratingVal = document.getElementById('ratingValue');

  if (!stars.length || !ratingVal) return;

  // Restore selected rating on page load (e.g. after validation error)
  const saved = parseInt(ratingVal.value);
  if (saved) fillStars(saved);

  stars.forEach(star => {
    star.addEventListener('mouseenter', () => {
      highlightStars(parseInt(star.dataset.value));
    });

    star.addEventListener('mouseleave', () => {
      fillStars(parseInt(ratingVal.value) || 0);
    });

    star.addEventListener('click', () => {
      const val = parseInt(star.dataset.value);
      ratingVal.value = val;
      fillStars(val);
    });
  });

  function highlightStars(count) {
    stars.forEach((s, i) => {
      s.classList.toggle('bi-star-fill', i < count);
      s.classList.toggle('bi-star', i >= count);
      s.classList.toggle('text-warning', i < count);
    });
  }

  function fillStars(count) {
    stars.forEach((s, i) => {
      s.classList.toggle('bi-star-fill', i < count);
      s.classList.toggle('bi-star', i >= count);
      s.classList.toggle('text-warning', i < count);
    });
  }

});


// ── Gallery filter & lightbox ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item');

  if (!filterBtns.length || !galleryItems.length) return;

  // ── Filter ──
  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      galleryItems.forEach((item) => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    });
  });

  // ── Lightbox ──
  const lightbox    = document.getElementById('galleryLightbox');
  const lbImg       = document.getElementById('galleryLightboxImg');
  const lbCaption   = document.getElementById('galleryLightboxCaption');
  const lbClose     = document.getElementById('galleryLightboxClose');

  if (!lightbox) return;

  galleryItems.forEach((item) => {
    item.addEventListener('click', () => {
      const img = item.querySelector('img');
      lbImg.src = img.src;
      lbImg.alt = img.alt;
      lbCaption.textContent = item.dataset.caption || '';
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  lbClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });

});


// ── Case study lightbox ────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  const caseLightbox = document.getElementById('caseLightbox');
  if (!caseLightbox) return;

  const lbClose       = document.getElementById('caseLightboxClose');
  const lbTitle       = document.getElementById('lbTitle');
  const lbClient      = document.getElementById('lbClient');
  const lbIndustry    = document.getElementById('lbIndustry');
  const lbSummary     = document.getElementById('lbSummary');
  const lbSummarySection = document.getElementById('lbSummarySection');
  const lbContent     = document.getElementById('lbContent');
  const lbDate        = document.getElementById('lbDate');

  // Open on "View Case" click
  document.querySelectorAll('.case-view-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();

      lbTitle.textContent    = btn.dataset.title    || '';
      lbClient.innerHTML     = `<i class="bi bi-building me-1"></i>${btn.dataset.client || ''}`;
      lbIndustry.textContent = btn.dataset.industry || '';
      lbContent.textContent  = btn.dataset.content  || '';
      lbDate.textContent     = btn.dataset.date      || '';

      const summary = btn.dataset.summary;
      if (summary) {
        lbSummary.textContent        = summary;
        lbSummarySection.style.display = '';
      } else {
        lbSummarySection.style.display = 'none';
      }

      caseLightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  function closeCaseLightbox() {
    caseLightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  lbClose.addEventListener('click', closeCaseLightbox);
  caseLightbox.addEventListener('click', (e) => {
    if (e.target === caseLightbox) closeCaseLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCaseLightbox();
  });

});

// ═══════════════════════════════════════════════════════════
// PUBLIC DARK MODE TOGGLE
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {

  const pubToggle = document.getElementById('pubDarkToggle');
  const pubIcon   = document.getElementById('pubDarkIcon');

  function applyPubTheme(isDark) {
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    if (pubIcon) pubIcon.className = isDark ? 'bi bi-sun' : 'bi bi-moon';
    localStorage.setItem('cn_pub_theme', isDark ? 'dark' : 'light');
  }

  if (pubToggle) {
    // Apply saved preference (anti-FOUC script already set the attribute,
    // this just syncs the icon)
    const saved = localStorage.getItem('cn_pub_theme');
    applyPubTheme(saved === 'dark');

    pubToggle.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') !== 'dark';
      applyPubTheme(isDark);
    });
  }

});