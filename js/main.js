/**
 * USNA Marine Detachment — main JavaScript
 * Vanilla ES6+, Cascade-compatible (no dependencies)
 */

(function () {
  'use strict';

  initMobileNav();
  initNavCloseOnLinkClick();

  /**
   * Toggle mobile navigation menu
   */
  function initMobileNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close menu on Escape key
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /**
   * Close mobile nav when a link is clicked (better UX on small screens)
   */
  function initNavCloseOnLinkClick() {
    var nav = document.querySelector('.site-nav');
    var toggle = document.querySelector('.nav-toggle');

    if (!nav || !toggle) return;

    nav.querySelectorAll('.site-nav__link').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 899px)').matches) {
          nav.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }
})();
