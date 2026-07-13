/**
 * Renders Marines on the Yard directory from window.MARINES_ON_THE_YARD
 * Company mentor section uses window.COMPANY_MENTORS (AY27 assignment list).
 */
(function () {
  'use strict';

  var container = document.getElementById('yard-directory');
  if (!container) return;

  var COMMUNITY_ORDER = [
    { id: 'mardet', label: 'Marine Detachment (MARDET)' },
    { id: 'mentor', label: 'Company Marine Mentors' },
    { id: 'company-officer', label: 'Company Officers' },
    { id: 'instructor', label: 'Academic Instructors' },
    { id: 'coach', label: 'Athletics & Extracurricular' },
    { id: 'support', label: "Commandant's Staff & Support" },
    { id: 'other', label: 'Other Marines on the Yard' }
  ];

  function sortMarines(a, b) {
    if (a.company && b.company) return a.company - b.company;
    return (a.name || '').localeCompare(b.name || '');
  }

  function companyLabel(n) {
    var suffix = 'th';
    if (n % 10 === 1 && n % 100 !== 11) suffix = 'st';
    else if (n % 10 === 2 && n % 100 !== 12) suffix = 'nd';
    else if (n % 10 === 3 && n % 100 !== 13) suffix = 'rd';
    return n + suffix + ' Company';
  }

  function appendRosterItem(ul, m) {
    var li = document.createElement('li');
    li.className = 'yard-roster__item';

    var title = document.createElement('p');
    title.className = 'yard-roster__name';
    title.textContent = (m.rank ? m.rank + ' ' : '') + m.name;
    li.appendChild(title);

    if (m.billet) {
      var billet = document.createElement('p');
      billet.className = 'yard-roster__detail';
      billet.textContent = m.billet;
      li.appendChild(billet);
    }

    var metaParts = [];
    if (m.company) metaParts.push(companyLabel(m.company));
    if (m.location) metaParts.push(m.location);
    if (m.department) metaParts.push(m.department);
    if (metaParts.length) {
      var meta = document.createElement('p');
      meta.className = 'yard-roster__meta';
      meta.textContent = metaParts.join(' · ');
      li.appendChild(meta);
    }

    if (m.notes) {
      var notes = document.createElement('p');
      notes.className = 'yard-roster__notes';
      notes.textContent = m.notes;
      li.appendChild(notes);
    }

    if (m.email || m.phone) {
      var contact = document.createElement('p');
      contact.className = 'yard-roster__contact';
      if (m.email) {
        var a = document.createElement('a');
        a.href = 'mailto:' + m.email;
        a.textContent = m.email;
        contact.appendChild(a);
      }
      if (m.email && m.phone) contact.appendChild(document.createTextNode(' · '));
      if (m.phone) contact.appendChild(document.createTextNode(m.phone));
      li.appendChild(contact);
    }

    ul.appendChild(li);
  }

  function renderMentorSection() {
    if (!window.COMPANY_MENTORS || !window.COMPANY_MENTORS.length) return false;

    var section = document.createElement('section');
    section.className = 'yard-group';
    section.id = 'yard-mentor';

    var heading = document.createElement('h2');
    heading.textContent = 'Company Marine Mentors';
    section.appendChild(heading);

    var intro = document.createElement('p');
    intro.className = 'yard-group__intro';
    intro.textContent = 'All 36 companies — AY27 Marine mentor assignments from the detachment roster.';
    section.appendChild(intro);

    var ul = document.createElement('ul');
    ul.className = 'yard-roster';

    window.COMPANY_MENTORS.slice().sort(sortMarines).forEach(function (mentor) {
      var dutyParts = [mentor.primaryDuty, mentor.collateralDuty, mentor.summerDuty].filter(Boolean);
      appendRosterItem(ul, {
        name: mentor.name,
        rank: mentor.rank,
        billet: mentor.primaryDuty || '',
        company: mentor.company,
        email: mentor.email,
        phone: '',
        notes: dutyParts.length > 1 ? dutyParts.slice(1).join(' · ') : '',
        location: '',
        department: ''
      });
    });

    section.appendChild(ul);
    container.appendChild(section);
    return true;
  }

  function renderFromDirectory() {
    if (!window.MARINES_ON_THE_YARD || !window.MARINES_ON_THE_YARD.length) return;

    var byCommunity = {};
    window.MARINES_ON_THE_YARD.forEach(function (m) {
      var key = m.community || 'other';
      if (key === 'mentor') return;
      if (!byCommunity[key]) byCommunity[key] = [];
      byCommunity[key].push(m);
    });

    COMMUNITY_ORDER.forEach(function (group) {
      if (group.id === 'mentor') return;
      var list = byCommunity[group.id];
      if (!list || !list.length) return;

      list.sort(sortMarines);

      var section = document.createElement('section');
      section.className = 'yard-group';
      section.id = 'yard-' + group.id;

      var heading = document.createElement('h2');
      heading.textContent = group.label;
      section.appendChild(heading);

      var ul = document.createElement('ul');
      ul.className = 'yard-roster';
      list.forEach(function (m) { appendRosterItem(ul, m); });

      section.appendChild(ul);
      container.appendChild(section);
    });
  }

  var hasMentors = renderMentorSection();
  renderFromDirectory();

  if (hasMentors || (window.MARINES_ON_THE_YARD && window.MARINES_ON_THE_YARD.length)) {
    var empty = document.getElementById('yard-directory-empty');
    if (empty) empty.hidden = true;
  }
})();
