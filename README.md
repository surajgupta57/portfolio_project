# Django Portfolio (fully admin-managed)

Every section of this site — navbar links, hero text, colors, fonts, experience
timeline, skills tabs, projects, education, testimonials, and contact info — is
stored in the database and editable from the Django admin. You should never need
to touch the templates or CSS to update your content or restructure sections
(add/remove/reorder timeline entries, skill tabs, projects, testimonials, nav
links, etc.).

## 1. Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_portfolio   # loads starter content so the site isn't empty
python manage.py runserver
```

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

`seed_portfolio` pre-fills the database with sample content (based on the
resume this project started from) purely so you have something to look at and
edit. Log into `/admin/` and change everything — your name, roles, projects,
colors, fonts — from there.

## 2. What's editable from the admin, and where

| Section | Admin model(s) |
|---|---|
| Fonts, colors, layout, meta info, footer | **⚙️ Site Settings** |
| Navbar links (add/remove/reorder, mark one as the CTA button) | **🧭 Navigation Links** |
| Hero name/role/description/buttons | **🏠 Hero Section — Profile** |
| Hero stat numbers (e.g. "6+ Years Experience") | **🏠 Hero Section — Stats** |
| Rotating hero widget cards | **🏠 Hero Section — Ledger Modules** (each has inline "lines") |
| About text | **👤 About Section — Text** |
| About skill chips | **👤 About Section — Skill Chips** |
| Experience timeline (bullets + tech tags edited inline on the same page) | **💼 Experience** |
| Skills tabs + the skills inside each tab (edited inline on the same page) | **🧩 Skills — Categories (Tabs)** |
| Projects (image, link, tech tags edited inline) | **🚀 Projects** |
| Education entries | **🎓 Education** |
| Testimonials (show/hide with a checkbox) | **💬 Testimonials** |
| Contact heading/lede + the mailto address the form sends to | **✉️ Contact — Section Text** |
| Contact detail rows (LinkedIn, email, phone, location, etc.) | **✉️ Contact — Info Lines** |

Every list model has an `order` field, editable straight from the list view
(no need to open each record) — that's how you reorder sections like
experience entries, projects, or nav links.

## 3. Adding/removing whole sections

Because sections are just querysets rendered with `{% if %}` / `{% for %}` in
`portfolio/templates/portfolio/index.html`, a section auto-hides itself when
its content is empty (e.g. delete all Testimonials and that section
disappears). To add a genuinely new *type* of section beyond what's modeled
here, you'd add a model + a small template block — but for everyday use
(new job, new project, new skill, restructure the nav, change every color)
you will only ever use the admin.

## 4. Colors & fonts

Open **Site Settings** in the admin:
- **Fonts**: type any Google Fonts family name exactly as shown on
  fonts.google.com (e.g. `Fraunces`, `Poppins`, `Inter`). The site pulls the
  correct Google Fonts `<link>` automatically — no code edits.
- **Colors**: hex codes for every color used across the site (background,
  ink/text, accent emerald, accent gold, etc.).
- **Layout**: max content width and vertical section padding.

## 5. Images

Upload a favicon, a résumé PDF, project screenshots, and testimonial photos
directly on their respective admin pages — they're stored under `/media/`.

## 6. Deploying

This ships with SQLite and `DEBUG=True` for local use. Before deploying:
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS`
  as environment variables.
- Point `DATABASES` at Postgres/MySQL if you want something more robust than
  SQLite.
- Run `python manage.py collectstatic` and serve `/static/` and `/media/`
  via your web server or a service like WhiteNoise/S3.

## Project layout

```
config/            # Django project settings/urls
portfolio/
  models.py         # every editable field on the site
  admin.py           # admin panel configuration (Jazzmin-powered UI)
  views.py            # single view that assembles all sections
  templates/
    base.html          # injects fonts/colors from Site Settings as CSS vars
    portfolio/index.html  # the page, built entirely from template loops
  static/portfolio/     # style.css + main.js (carousels, tabs, nav, form)
  management/commands/seed_portfolio.py   # optional starter content
```
