/**
 * Renders company mentor cards from window.COMPANY_MENTORS
 */
(function () {
  'use strict';

  var grid = document.getElementById('mentor-grid');
  var filters = document.querySelectorAll('.mentor-filter');

  if (!grid || !window.COMPANY_MENTORS) return;

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildDutyList(mentor) {
    var items = [
      { label: 'Primary Duty', value: mentor.primaryDuty || mentor.bio },
      { label: 'Collateral Duty', value: mentor.collateralDuty },
      { label: '2026 Summer Duty', value: mentor.summerDuty }
    ].filter(function (item) {
      return item.value && String(item.value).trim();
    });

    if (!items.length) {
      return '<p class="mentor-card__bio is-placeholder">Duty information coming soon.</p>';
    }

    return (
      '<dl class="mentor-card__duties">' +
      items.map(function (item) {
        return (
          '<div class="mentor-card__duty">' +
            '<dt>' + escapeHtml(item.label) + '</dt>' +
            '<dd>' + escapeHtml(item.value) + '</dd>' +
          '</div>'
        );
      }).join('') +
      '</dl>'
    );
  }

  function renderCards(battalion) {
    grid.innerHTML = '';

    window.COMPANY_MENTORS.forEach(function (mentor) {
      if (battalion !== 'all' && String(mentor.battalion) !== battalion) return;

      var card = document.createElement('article');
      card.className = 'mentor-card';
      card.id = 'company-' + mentor.company;

      var photoAlt = mentor.name
        ? 'Portrait of ' + mentor.rank + ' ' + mentor.name
        : 'Company ' + mentor.company + ' Marine mentor';

      var photoHtml =
        '<img src="' + mentor.photo + '" alt="' + photoAlt + '" ' +
        'onerror="this.replaceWith(Object.assign(document.createElement(\'span\'),{innerHTML:\'Photo pending<br>Company ' + mentor.company + '\'}));">';

      var displayName = mentor.name
        ? mentor.rank + ' ' + mentor.name
        : 'Marine Company Mentor';

      var emailHtml = mentor.email
        ? '<p class="mentor-card__meta"><a href="mailto:' + mentor.email + '">' + escapeHtml(mentor.email) + '</a></p>'
        : '';

      card.innerHTML =
        '<div class="mentor-card__photo">' + photoHtml + '</div>' +
        '<div class="mentor-card__body">' +
          '<p class="mentor-card__company">Company ' + mentor.company + ' · ' + mentor.battalion + getOrdinal(mentor.battalion) + ' Battalion</p>' +
          '<h3 class="mentor-card__name">' + escapeHtml(displayName) + '</h3>' +
          emailHtml +
          buildDutyList(mentor) +
        '</div>';

      grid.appendChild(card);
    });
  }

  function getOrdinal(n) {
    var suffix = 'th';
    if (n % 10 === 1 && n % 100 !== 11) suffix = 'st';
    else if (n % 10 === 2 && n % 100 !== 12) suffix = 'nd';
    else if (n % 10 === 3 && n % 100 !== 13) suffix = 'rd';
    return suffix;
  }

  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filters.forEach(function (b) {
        b.classList.remove('is-active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-pressed', 'true');
      renderCards(btn.getAttribute('data-battalion'));
    });
  });

  renderCards('all');
})();
