---
layout: page
title: Athletics
bg: athletics
chapter: "Athletics"
page_bg: athletics
subtitle: "Varsity distance runner · Track & Field and Cross Country · consistent 7–10% improvement every season."
permalink: /athletics/
---

<!-- Sub-nav (#3) -->
<nav class="subnav" aria-label="Athletics sections">
  <div class="subnav-inner">
    <a href="#stats"       class="subnav-link">Stats</a>
    <a href="#progression" class="subnav-link">Progression</a>
    <a href="#records"     class="subnav-link">PRs</a>
    <a href="#awards"      class="subnav-link">Awards</a>
    <a href="#video"       class="subnav-link">Video</a>
  </div>
</nav>

<div class="section">
  <div id="stats" class="section-anchor"></div>
  <div class="stat-cards">
    <div class="stat-card">
      <div class="stat-card-val">11:40 <span class="stat-card-unit">3200m</span></div>
      <div class="stat-card-lbl">19th in Class 3A · Outdoor</div>
      <div class="stat-card-delta">↓ 6.7% this season</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-val">19:34 <span class="stat-card-unit">5K XC</span></div>
      <div class="stat-card-lbl">State qualifier · 2025</div>
      <div class="stat-card-delta">↓ 9.9% this season</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-val">5:11 <span class="stat-card-unit">1600m</span></div>
      <div class="stat-card-lbl">24th in Class 3A · Outdoor</div>
      <div class="stat-card-delta">↓ 8.5% this season</div>
    </div>
  </div>

  <div id="progression" class="section-anchor"></div>
  <span class="section-label">Season progression</span>
  {% include athletics-chart.html %}

  <!-- Sortable PR table (#8) -->
  <div id="records" class="section-anchor"></div>
  <span class="section-label">Personal records <span class="sortable-hint">click column header to sort</span></span>
  <div class="ruled-table sortable-table" id="pr-table" style="margin-bottom:2.5rem;">
    <div class="ruled-head pr-head" style="grid-template-columns:2rem 1fr 1fr auto;">
      <span></span>
      <span class="sort-col" data-col="0" data-type="text" aria-sort="none">Event <span class="sort-icon">⇅</span></span>
      <span class="sort-col" data-col="1" data-type="time" aria-sort="none">PR <span class="sort-icon">⇅</span></span>
      <span class="sort-col" data-col="2" data-type="text" aria-sort="none">Rank <span class="sort-icon">⇅</span></span>
    </div>
    <div class="pr-tbody">
      <div class="ruled-row pr-row" style="grid-template-columns:2rem 1fr 1fr auto;" data-event="3200m" data-time="11:40.53" data-rank="19th · 3A">
        <span class="ruled-num">01</span>
        <span class="ruled-name">3200m</span>
        <span class="ruled-meta pr-time" style="color:#3d5a6e;font-weight:700;">11:40.53</span>
        <span class="ruled-badge">19th · 3A</span>
      </div>
      <div class="ruled-row pr-row" style="grid-template-columns:2rem 1fr 1fr auto;" data-event="1600m" data-time="5:11.67" data-rank="24th · 3A">
        <span class="ruled-num">02</span>
        <span class="ruled-name">1600m</span>
        <span class="ruled-meta pr-time" style="color:#3d5a6e;font-weight:700;">5:11.67</span>
        <span class="ruled-badge">24th · 3A</span>
      </div>
      <div class="ruled-row pr-row" style="grid-template-columns:2rem 1fr 1fr auto;" data-event="800m" data-time="2:25.16" data-rank="30th · 3A">
        <span class="ruled-num">03</span>
        <span class="ruled-name">800m</span>
        <span class="ruled-meta">2:25.16</span>
        <span class="ruled-badge">30th · 3A</span>
      </div>
      <div class="ruled-row pr-row" style="grid-template-columns:2rem 1fr 1fr auto;" data-event="5K Cross Country" data-time="19:34.42" data-rank="State qualifier">
        <span class="ruled-num">04</span>
        <span class="ruled-name">5K Cross Country</span>
        <span class="ruled-meta">19:34.42</span>
        <span class="ruled-badge">State qualifier</span>
      </div>
      <div class="ruled-row pr-row" style="grid-template-columns:2rem 1fr 1fr auto;" data-event="400m" data-time="1:00.61" data-rank="—">
        <span class="ruled-num">05</span>
        <span class="ruled-name">400m</span>
        <span class="ruled-meta">1:00.61</span>
        <span class="ruled-badge">—</span>
      </div>
    </div>
  </div>
  <div id="awards" class="section-anchor"></div>
  <span class="section-label">Awards & recognition</span>
  <div class="info-grid" style="border:1px solid var(--border-dark);border-radius:var(--radius);overflow:hidden;">
    <div class="info-cell"><div class="info-pip"></div><div>
      <div class="info-cell-title">Athlete of the Meet</div>
      <div class="info-cell-sub">ASCTE · 2nd ever recipient</div>
    </div></div>
    <div class="info-cell"><div class="info-pip"></div><div>
      <div class="info-cell-title">AHSAA 3A State XC Qualifier</div>
      <div class="info-cell-sub">2025 season</div>
    </div></div>
    <div class="info-cell"><div class="info-pip"></div><div>
      <div class="info-cell-title">4th in Section 4 — 3200m</div>
      <div class="info-cell-sub">2026 Outdoor</div>
    </div></div>
    <div class="info-cell"><div class="info-pip"></div><div>
      <div class="info-cell-title">NCAA ID: 2504562826</div>
      <div class="info-cell-sub"><a href="{{ site.milesplit_url }}" target="_blank" rel="noopener">View MileSplit profile →</a></div>
    </div></div>
  </div>

  <div id="video" class="section-anchor"></div>
  <span class="section-label" style="margin-top:2.5rem;display:block;">Race footage</span>
  <div class="video-section">
    <div class="video-frame" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;">
      <iframe
        src="https://drive.google.com/file/d/1JXoG2tSdJvHGkTJcPpji8noB6NWoGxhQ/preview"
        style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
        allow="autoplay"
        allowfullscreen>
      </iframe>
    </div>
    <div class="video-meta">
      <div class="video-meta-text">
        <div class="video-meta-title">Mile PR Run — Indoor Track 2026</div>
        <div class="video-meta-sub">
          ASCTE Indoor Invitational · 5:15.81<br>
          Regulated pacing to slowly overtake every runner — the best race of the season
        </div>
      </div>
      <a href="https://drive.google.com/file/d/1JXoG2tSdJvHGkTJcPpji8noB6NWoGxhQ/view?usp=sharing"
         target="_blank" rel="noopener" class="video-download-btn">
        ↓ Full quality video
      </a>
    </div>
  </div>
</div>

<!-- Sortable PR table JS (#8) -->
<script>
(function() {
  var tbody = document.querySelector('.pr-tbody');
  var headers = document.querySelectorAll('.sort-col');
  if (!tbody || !headers.length) return;

  function timeToSeconds(t) {
    if (!t || t === '—') return Infinity;
    var parts = t.split(':').map(parseFloat);
    return parts.length === 2 ? parts[0] * 60 + parts[1] : parts[0];
  }

  var sortState = { col: null, asc: true };

  headers.forEach(function(th) {
    th.style.cursor = 'pointer';
    th.addEventListener('click', function() {
      var col = th.getAttribute('data-col');
      var type = th.getAttribute('data-type');
      if (sortState.col === col) { sortState.asc = !sortState.asc; }
      else { sortState.col = col; sortState.asc = true; }

      headers.forEach(function(h) {
        h.setAttribute('aria-sort', 'none');
        h.querySelector('.sort-icon').textContent = '⇅';
      });
      th.setAttribute('aria-sort', sortState.asc ? 'ascending' : 'descending');
      th.querySelector('.sort-icon').textContent = sortState.asc ? '↑' : '↓';

      var rows = Array.from(tbody.querySelectorAll('.pr-row'));
      rows.sort(function(a, b) {
        var aVal, bVal;
        if (col === '0') { aVal = a.getAttribute('data-event'); bVal = b.getAttribute('data-event'); }
        else if (col === '1') { aVal = timeToSeconds(a.getAttribute('data-time')); bVal = timeToSeconds(b.getAttribute('data-time')); return sortState.asc ? aVal - bVal : bVal - aVal; }
        else { aVal = a.getAttribute('data-rank'); bVal = b.getAttribute('data-rank'); }
        return sortState.asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      });

      rows.forEach(function(r, i) {
        r.querySelector('.ruled-num').textContent = String(i + 1).padStart(2, '0');
        tbody.appendChild(r);
      });
    });
  });
})();
</script>

<!-- Scroll-spy sub-nav (#3) -->
<script>
(function() {
  var links = document.querySelectorAll('.subnav-link');
  var sections = Array.from(links).map(function(l) {
    return document.getElementById(l.getAttribute('href').slice(1));
  });
  if (!links.length || !sections.length) return;
  var navH = document.querySelector('.site-nav') ? document.querySelector('.site-nav').offsetHeight : 58;
  var subH = document.querySelector('.subnav') ? document.querySelector('.subnav').offsetHeight : 38;

  function spy() {
    var scrollY = window.scrollY + navH + subH + 20;
    var active = 0;
    sections.forEach(function(s, i) { if (s && s.offsetTop <= scrollY) active = i; });
    links.forEach(function(l, i) { l.classList.toggle('active', i === active); });
  }

  window.addEventListener('scroll', spy, { passive: true });
  spy();
})();
</script>
