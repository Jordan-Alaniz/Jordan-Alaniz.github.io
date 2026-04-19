# Personal Website

This is the source code for my personal website, built with Jekyll and the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme, hosted on GitHub Pages.

Full disclosure: I'm a busy high school student, and used GitHub Copilot to help design the structure and set up my website, but all of the content you see is original and mine! My website is still a work in progress, and I add to it whenever I can, so please excuse parts that may not be complete or long pauses in between contributions. Enjoy!

Check it out live here: [https://Jordan-Alaniz.github.io/](https://Jordan-Alaniz.github.io/)

---

## How to Add Content

### Adding a Blog Post

1. Create a new file in the `_posts/` directory.
2. Name it using the format: `YYYY-MM-DD-title-of-post.md`  
   Example: `_posts/2025-03-01-my-new-post.md`
3. Add the following front matter at the top:

```yaml
---
title: "My Post Title"
date: 2025-03-01
categories:
  - Technical         # or General, Athletics, etc.
tags:
  - Python            # any relevant tags
---

Your post content goes here in Markdown...
```

### Adding a Project

1. Create a new file in the `_projects/` directory.
2. Name it with a short descriptive slug: `_projects/my-project.md`
3. Add the following front matter at the top:

```yaml
---
title: "My Project Title"
excerpt: "One sentence description shown on the projects grid."
date: 2025-03-01
tags:
  - Python
  - Hardware
header:
  teaser: /assets/images/projects/my-project-teaser.jpg   # optional thumbnail (600x400px recommended)
---

## Overview
...

## Tools & Skills Used
...

## What I Learned
...
```

4. (Optional) Add a teaser image at `assets/images/projects/my-project-teaser.jpg` — a 600×400px image works well.

### Updating Your Resume

- **Academic Resume:** Edit `_pages/resume.md`
- **Athletic Resume:** Edit `_pages/athletic-resume.md`
- **PDF Download:** Replace `assets/files/Jordan_Alaniz_Resume.pdf` with your updated PDF.

### Adding Dynamic Visual Content (Markdown Only)

You can add richer visual components to any page just by editing its `.md` file — no HTML required.

#### Feature Rows (cards with buttons)

Add a `feature_row` block to any page's front matter, then call `{% include feature_row %}` in the body:

```yaml
---
feature_row:
  - title: "Section Title"
    excerpt: "A short description of this section."
    url: "/some-page/"
    btn_label: "Go There"
    btn_class: "btn--primary"   # or btn--inverse, btn--warning, etc.
  - title: "Another Section"
    excerpt: "Another description."
    url: "/other-page/"
    btn_label: "Read More"
    btn_class: "btn--primary"
    image_path: /assets/images/my-image.jpg   # optional thumbnail
---

{% include feature_row %}
```

#### Notice Boxes

Wrap any paragraph with a notice class for a highlighted callout:

```markdown
This is an informational note.
{: .notice--info}

This is a warning.
{: .notice--warning}

This is a success message.
{: .notice--success}
```

Available styles: `notice`, `notice--primary`, `notice--info`, `notice--warning`, `notice--success`, `notice--danger`.

### Repository Structure

```
_posts/          <- Blog posts (YYYY-MM-DD-title.md)
_projects/       <- Project writeups
_pages/          <- Static pages (resume, about, blog index, etc.)
assets/
  files/         <- Downloadable files (PDF resume, etc.)
  images/
    projects/    <- Project teaser images
_data/
  navigation.yml <- Site navigation links
_config.yml      <- Site-wide settings
```
