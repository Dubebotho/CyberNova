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

  const filterBtns   = document.querySelectorAll('.gallery-filter-btn');
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
  const lightbox  = document.getElementById('galleryLightbox');
  const lbImg     = document.getElementById('galleryLightboxImg');
  const lbCaption = document.getElementById('galleryLightboxCaption');
  const lbClose   = document.getElementById('galleryLightboxClose');

  if (!lightbox) return;

  galleryItems.forEach((item) => {
    item.addEventListener('click', () => {
      const img  = item.querySelector('img');
      lbImg.src  = img.src;
      lbImg.alt  = img.alt;
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

  const lbClose          = document.getElementById('caseLightboxClose');
  const lbTitle          = document.getElementById('lbTitle');
  const lbClient         = document.getElementById('lbClient');
  const lbIndustry       = document.getElementById('lbIndustry');
  const lbSummary        = document.getElementById('lbSummary');
  const lbSummarySection = document.getElementById('lbSummarySection');
  const lbContent        = document.getElementById('lbContent');
  const lbDate           = document.getElementById('lbDate');

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
        lbSummary.textContent          = summary;
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
    if (pubIcon)   pubIcon.className = isDark ? 'bi bi-sun' : 'bi bi-moon';
    // Keep data-label in sync so the CSS ::after label reads correctly on mobile
    if (pubToggle) pubToggle.setAttribute('data-label', isDark ? 'Light Mode' : 'Dark Mode');
    localStorage.setItem('cn_pub_theme', isDark ? 'dark' : 'light');
  }

  if (pubToggle) {
    // Apply saved preference on load (anti-FOUC script already set the
    // data-theme attribute; this syncs the icon and data-label)
    const saved = localStorage.getItem('cn_pub_theme');
    applyPubTheme(saved === 'dark');

    pubToggle.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') !== 'dark';
      applyPubTheme(isDark);
    });
  }

});


// ═══════════════════════════════════════════════════════════
// ADMIN DARK MODE TOGGLE
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {

  const toggle = document.getElementById('darkModeToggle');
  const icon   = document.getElementById('darkModeIcon');
  const label  = document.getElementById('darkModeLabel');

  function applyAdminTheme(isDark) {
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    if (icon)  icon.className    = isDark ? 'bi bi-sun'    : 'bi bi-moon';
    if (label) label.textContent = isDark ? 'Light Mode'   : 'Dark Mode';
    localStorage.setItem('cn_theme', isDark ? 'dark' : 'light');
  }

  if (toggle) {
    // Sync icon & label with whatever the anti-FOUC <head> script already applied
    const saved = localStorage.getItem('cn_theme');
    applyAdminTheme(saved === 'dark');

    toggle.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') !== 'dark';
      applyAdminTheme(isDark);
    });
  }

});


// ═══════════════════════════════════════════════════════════
// SIDEBAR MOBILE TOGGLE
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {

  const sidebarToggle  = document.getElementById('sidebarToggle');
  const adminSidebar   = document.getElementById('adminSidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (!sidebarToggle || !adminSidebar || !sidebarOverlay) return;

  function openSidebar() {
    adminSidebar.classList.add('open');
    sidebarOverlay.classList.add('open');
  }

  function closeSidebar() {
    adminSidebar.classList.remove('open');
    sidebarOverlay.classList.remove('open');
  }

  sidebarToggle.addEventListener('click', openSidebar);
  sidebarOverlay.addEventListener('click', closeSidebar);

  // Also close sidebar on Escape key (accessibility)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && adminSidebar.classList.contains('open')) {
      closeSidebar();
    }
  });

});



// ═══════════════════════════════════════════════════════════
// MOST REQUESTED SERVICES CHART
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {

  const canvas = document.getElementById('servicesChart');
  if (!canvas) return;

  // Data is embedded in data-* attributes by the Jinja template
  let labels, values;
  try {
    labels = JSON.parse(canvas.dataset.labels || '[]');
    values = JSON.parse(canvas.dataset.values || '[]');
  } catch (e) {
    console.error('servicesChart: failed to parse data attributes', e);
    return;
  }

  if (!labels.length || !values.length) return;

  // ── Brand palette — cycles if there are more bars than colours ──
  const PALETTE = [
    '#002B5B', '#10B981', '#3B82F6', '#F59E0B',
    '#8B5CF6', '#EF4444', '#06B6D4', '#EC4899',
  ];

  function buildColors(count) {
    return Array.from({ length: count }, (_, i) => PALETTE[i % PALETTE.length]);
  }

  // ── Detect dark mode ────────────────────────────────────
  function isDark() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  function chartColors() {
    return {
      gridColor  : isDark() ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
      tickColor  : isDark() ? '#64748b'                : '#94a3b8',
      tooltipBg  : isDark() ? '#1e293b'                : '#ffffff',
      tooltipText: isDark() ? '#e2e8f0'                : '#0f172a',
    };
  }

  // ── Fix: wrap canvas in a fixed-height container ────────
  // Chart.js with responsive:true measures its *parent* element
  // to determine size. If the parent has no fixed height, a
  // tooltip hover triggers a resize feedback loop that shrinks
  // the canvas to zero. Wrapping in a div with an explicit
  // pixel height and setting maintainAspectRatio:false breaks
  // the loop and locks the chart to that height.
  const wrapper = document.createElement('div');
  wrapper.style.cssText = 'position:relative;width:100%;height:260px;';
  canvas.parentNode.insertBefore(wrapper, canvas);
  wrapper.appendChild(canvas);

  // ── Build chart ─────────────────────────────────────────
  const ctx = canvas.getContext('2d');
  const c   = chartColors();

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label          : 'Requests',
        data           : values,
        backgroundColor: buildColors(values.length),
        borderRadius   : 6,
        borderSkipped  : false,
        barThickness   : 'flex',
        maxBarThickness: 52,
      }],
    },
    options: {
      responsive         : true,
      maintainAspectRatio: false,   // false is required when parent has a fixed height
      animation          : { duration: 400 },
      plugins: {
        legend : { display: false },
        tooltip: {
          backgroundColor: c.tooltipBg,
          titleColor     : c.tooltipText,
          bodyColor      : c.tooltipText,
          borderColor    : isDark() ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)',
          borderWidth    : 1,
          padding        : 10,
          callbacks: {
            label: (item) => ` ${item.parsed.y} request${item.parsed.y !== 1 ? 's' : ''}`,
          },
        },
      },
      scales: {
        x: {
          grid : { display: false },
          ticks: {
            color      : c.tickColor,
            font       : { family: 'Inter, sans-serif', size: 11 },
            maxRotation: 30,
          },
          border: { color: c.gridColor },
        },
        y: {
          beginAtZero: true,
          grid       : { color: c.gridColor },
          ticks      : {
            color    : c.tickColor,
            font     : { family: 'Inter, sans-serif', size: 11 },
            stepSize : 1,
            precision: 0,
          },
          border: { color: c.gridColor, dash: [4, 4] },
        },
      },
    },
  });

  // ── Re-theme chart when dark mode is toggled ────────────
  const observer = new MutationObserver(() => {
    const c = chartColors();
    chart.options.plugins.tooltip.backgroundColor = c.tooltipBg;
    chart.options.plugins.tooltip.titleColor      = c.tooltipText;
    chart.options.plugins.tooltip.bodyColor       = c.tooltipText;
    chart.options.plugins.tooltip.borderColor     = isDark()
      ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';
    chart.options.scales.x.ticks.color  = c.tickColor;
    chart.options.scales.x.border.color = c.gridColor;
    chart.options.scales.y.grid.color   = c.gridColor;
    chart.options.scales.y.ticks.color  = c.tickColor;
    chart.options.scales.y.border.color = c.gridColor;
    chart.update('none'); // 'none' skips animation on theme switch
  });

  observer.observe(document.documentElement, {
    attributes     : true,
    attributeFilter: ['data-theme'],
  });

});

// ═══════════════════════════════════════════════════════════
// INQUIRY MODALS
// ═══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {

  // ── View Modal ──────────────────────────────────────────
  const viewModal = document.getElementById('viewInquiryModal');
  if (viewModal) {
    viewModal.addEventListener('show.bs.modal', (e) => {
      const btn = e.relatedTarget;

      document.getElementById('viewModalName').textContent      = btn.dataset.name || 'Inquiry Details';
      document.getElementById('viewModalSubmitted').textContent = btn.dataset.submitted || '';
      document.getElementById('viewModalNameVal').textContent   = btn.dataset.name    || '—';
      document.getElementById('viewModalCompany').textContent   = btn.dataset.company || '—';
      document.getElementById('viewModalEmail').textContent     = btn.dataset.email   || '—';
      document.getElementById('viewModalPhone').textContent     = btn.dataset.phone   || '—';
      document.getElementById('viewModalMessage').textContent   = btn.dataset.message || '—';

      const status = btn.dataset.status || '';
      const badge  = document.getElementById('viewModalStatusBadge');
      badge.className = `status-badge status-${status.toLowerCase().replace(' ', '_')}`;
      document.getElementById('viewModalStatus').textContent = status.toUpperCase();

      const svc = document.getElementById('viewModalService');
      svc.textContent    = btn.dataset.service || '—';
      svc.style.display  = btn.dataset.service ? '' : 'none';
    });
  }

  // ── Edit Modal ──────────────────────────────────────────
  const editModal = document.getElementById('editInquiryModal');
  if (editModal) {
    editModal.addEventListener('show.bs.modal', (e) => {
      const btn = e.relatedTarget;
      document.getElementById('editModalName').textContent = btn.dataset.name   || '';
      document.getElementById('editModalStatus').value     = btn.dataset.status || 'new';
      document.getElementById('editInquiryForm').action   = `/admin/inquiries/${btn.dataset.id}/status`;
    });
  }

});

// ── Custom confirm modal ───────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const modalEl = document.getElementById('confirmModal');
  if (!modalEl) return;                              // ← guard added

  const modal     = new bootstrap.Modal(modalEl);
  const msgEl     = document.getElementById('confirmModalMessage');
  const okBtn     = document.getElementById('confirmModalOk');
  let pendingForm = null;

  document.querySelectorAll('form[data-confirm]').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      msgEl.textContent = form.dataset.confirm;
      pendingForm = form;
      modal.show();
    });
  });

  okBtn.addEventListener('click', () => {
    if (pendingForm) {
      pendingForm.submit();
      pendingForm = null;
    }
    modal.hide();
  });
});

history.pushState(null, '', window.location.href);
window.addEventListener('popstate', () => {
  history.pushState(null, '', window.location.href);
});