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
  training_log.json <- Auto-updated by Garmin sync workflow
_config.yml      <- Site-wide settings
scripts/
  fetch_garmin.py         <- Pulls activities from Garmin Connect (run by CI)
  export_garmin_token.py  <- One-time local script to generate GARMIN_TOKENSTORE secret
```

---

## Garmin Training Log Sync

The training log on the Athletics page is automatically updated daily from Garmin Connect.

### How it works

1. A GitHub Actions workflow (`.github/workflows/sync-garmin.yml`) runs every day at 1:00 AM CT.
2. It runs `scripts/fetch_garmin.py`, which pulls recent running activities from Garmin Connect and writes `_data/training_log.json`.
3. If the file changed, the workflow commits and pushes it, which triggers a new GitHub Pages build.

### One-time setup: create the `GARMIN_TOKENSTORE` secret

Because Garmin uses MFA-style OAuth, you need to generate a token once on your local machine and store it as a GitHub secret. The workflow uses this token instead of your password.

**Step 1 — Generate the token locally:**

```bash
pip install garth
python scripts/export_garmin_token.py
```

Enter your Garmin email and password when prompted. The script will print a long base64 string.

**Step 2 — Add it as a GitHub secret:**

1. Go to your repo on GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GARMIN_TOKENSTORE`
4. Value: paste the base64 string from Step 1
5. Click **Add secret**

After this, the workflow will use the token automatically. You no longer need `GARMIN_EMAIL` or `GARMIN_PASSWORD` secrets (though the workflow supports them as a fallback if `GARMIN_TOKENSTORE` is not set).

### Triggering a manual sync

Go to **Actions** → **Sync Garmin Training Log** → **Run workflow**.
