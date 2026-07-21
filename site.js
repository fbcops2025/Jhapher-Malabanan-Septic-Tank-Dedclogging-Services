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
    'septic-tank-warning-signs': 'guides',
  };
  const activePage = groups[page] || page;
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
