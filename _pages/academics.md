---
layout: page
title: Academics
bg: academics
chapter: "Academics"
page_bg: academics
subtitle: "ASCTE junior · 4.29 GPA · All courses Honors or AP level · focused on engineering and cybersecurity."
permalink: /academics/
---

<div class="section">
  <div class="stat-cards">
    <div class="stat-card">
      <div class="stat-card-val">4.29 <span class="stat-card-unit">GPA</span></div>
      <div class="stat-card-lbl">Weighted · All Honors/AP</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-val">1310 <span class="stat-card-unit">SAT</span></div>
      <div class="stat-card-lbl">680 Reading · 630 Math</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-val">32 <span class="stat-card-unit">ACT</span></div>
      <div class="stat-card-lbl">34 English/Reading · 29 Math</div>
    </div>
  </div>

  <span class="section-label">Current AP courses</span>
  <div class="info-grid" style="margin-bottom:2.5rem;border:1px solid var(--border-dark);border-radius:var(--radius);overflow:hidden;">
    <div class="info-cell"><div class="info-pip"></div><div><div class="info-cell-title">AP Computer Science A</div><div class="info-cell-sub">Java · algorithms · OOP</div></div></div>
    <div class="info-cell"><div class="info-pip"></div><div><div class="info-cell-title">AP Calculus</div><div class="info-cell-sub">Derivatives · integration</div></div></div>
    <div class="info-cell"><div class="info-pip"></div><div><div class="info-cell-title">AP Psychology</div><div class="info-cell-sub">Behavioral science</div></div></div>
    <div class="info-cell"><div class="info-pip"></div><div><div class="info-cell-title">AP Language</div><div class="info-cell-sub">Completed sophomore year</div></div></div>
  </div>
  <span class="section-label">Projects</span>
  <div class="project-grid">
    {% assign projects = site.projects | sort: "date" | reverse %}
    {% for project in projects %}
    <a href="{{ project.url | relative_url }}" class="project-card">
      <span class="project-card-year">{{ project.date | date: "%Y" }} &mdash; {{ project.categories | first | default: "ASCTE" }}</span>
      {% if project.status %}<span class="status-badge status-{{ project.status | downcase | replace: ' ', '-' }}">{{ project.status }}</span>{% endif %}
      <span class="project-card-title">{{ project.title }}</span>
      <p class="project-card-excerpt">{{ project.excerpt | strip_html | truncate: 120 }}</p>
      <div class="project-card-tags">
        {% for tag in project.tags limit:4 %}<span class="tag">{{ tag }}</span>{% endfor %}
      </div>
    </a>
    {% endfor %}
  </div>

  <span class="section-label">Skills</span>
  <div class="ruled-table" style="--cols:1fr 1fr 1fr;">
    <div class="ruled-head" style="grid-template-columns:1fr 1fr 1fr;"><span>Language / Tool</span><span>Context</span><span>Level</span></div>
    <div class="ruled-row" style="grid-template-columns:1fr 1fr 1fr;"><span class="ruled-name">Python</span><span class="ruled-meta">Algorithms, scripting, networking</span><span class="ruled-badge">Advanced</span></div>
    <div class="ruled-row" style="grid-template-columns:1fr 1fr 1fr;"><span class="ruled-name">Java</span><span class="ruled-meta">AP CS A, OOP</span><span class="ruled-badge">Intermediate</span></div>
    <div class="ruled-row" style="grid-template-columns:1fr 1fr 1fr;"><span class="ruled-name">HTML · CSS · JS</span><span class="ruled-meta">Web projects</span><span class="ruled-badge">Intermediate</span></div>
    <div class="ruled-row" style="grid-template-columns:1fr 1fr 1fr;"><span class="ruled-name">Linux · Networking</span><span class="ruled-meta">CTF, cluster setup</span><span class="ruled-badge">Foundational</span></div>
    <div class="ruled-row" style="grid-template-columns:1fr 1fr 1fr;"><span class="ruled-name">Fusion 360</span><span class="ruled-meta">CAD, engineering curriculum</span><span class="ruled-badge">Foundational</span></div>
  </div>
</div>
