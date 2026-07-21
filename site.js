(() => {
  const button = document.querySelector('.menu-button');
  const navigation = document.querySelector('.primary-nav');

  if (button && navigation) {
    button.addEventListener('click', () => {
      const open = navigation.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
    });

    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) {
        navigation.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const page = document.body.dataset.page;
  const groups = {
    'septic-tank-siphoning': 'services',
    'pozo-negro-cleaning': 'services',
    'declogging-services': 'services',
    'metro-manila': 'service-areas',
    rizal: 'service-areas',
    'cavite-laguna': 'service-areas',
    guides: 'blog',
  };
  const blogPages = new Set([
    'blog',
    'septic-tank-warning-signs',
    'siphoning-vs-declogging',
    'barado-ang-cr-ano-gagawin',
    'how-often-septic-tank-siphoning',
    'mabaho-ang-drain-sanhi-solusyon',
    'prepare-for-septic-siphoning',
    'septic-overflow-emergency-steps',
    'pozo-negro-vs-septic-tank',
    'slow-drains-multiple-fixtures',
    'what-not-to-flush-septic',
    'rainy-season-septic-problems',
    'gurgling-toilet-meaning',
    'wet-ground-near-septic-tank',
    'apartment-building-drain-problems',
    'restaurant-kitchen-drain-care',
    'landlord-septic-maintenance-checklist',
    'manhole-access-for-siphoning',
    'after-siphoning-what-to-expect',
    'floor-drain-backup-causes',
    'commercial-property-declogging-guide',
    'septic-tank-odor-outside-house',
    'blocked-sink-vs-septic-issue',
    'how-to-describe-clog-for-faster-help',
    'pasig-septic-service-what-to-expect',
  ]);
  const activePage = blogPages.has(page) ? 'blog' : (groups[page] || page);
  const activeLink = document.querySelector(`[data-page="${activePage}"]`);
  if (activeLink) activeLink.setAttribute('aria-current', 'page');

  const mobileActions = document.querySelector('.mobile-actions');
  if (mobileActions) {
    const updateMobileActions = () => {
      mobileActions.classList.toggle('visible', window.scrollY > 520);
    };
    updateMobileActions();
    window.addEventListener('scroll', updateMobileActions, { passive: true });
  }
})();
