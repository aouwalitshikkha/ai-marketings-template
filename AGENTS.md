# aimrarket — AGENTS.md

## Quick start
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# CSS (optional — for Tailwind edits):
npm install          # installs tailwindcss + @tailwindcss/cli
npm run dev          # watch: rebuilds static/css/output.css on change
npm run build        # one-time build
```

## Architecture
- **Django 5.2** project with 6 apps: `blog`, `glossary`, `top10s`, `courses`, `pages`, `search`
- **15 Django templates** (1 base + 14 page templates), extends pattern
- **Tailwind CSS v4** via `@tailwindcss/cli` — no `tailwind.config.js`, no PostCSS
- Entry CSS: `src/input.css` — only `@import "tailwindcss"` + `focus-visible` styles
- Output: `static/css/output.css` — **committed** (served via `{% static %}`)
- All placeholder images from picsum.photos
- Static JS: `static/js/search-toggle.js`, `static/js/blog-post.js`, `static/js/glossary.js`

## Template map
```
templates/
├── base.html                 shared layout (nav, footer, search bar)
├── home.html                 landing page
├── pages/
│   ├── about.html            about us
│   ├── contact.html          contact form
│   └── privacy.html          privacy policy
├── top10s/
│   ├── profile_list.html     Top 10 landing (listicle cards + pagination)
│   └── profile_detail.html   single Top 10 listicle (10 items)
├── courses/
│   ├── course_list.html      course catalog (level filter)
│   ├── course_detail.html    single course detail (syllabus)
│   └── chapter_detail.html   single chapter/lesson
├── search/
│   └── search.html           server-side search (reads ?q= parameter)
├── blog/
│   └── templates/blog/
│       ├── post_list.html    blog home (category pills + post grid + sidebar)
│       ├── post_detail.html  single blog post
│       └── category.html     category-filtered posts
└── glossary/
    └── templates/glossary/
        ├── index.html        AI marketing glossary (expandable terms)
        └── glossary.md       markdown export template
```

## Nav — shared via `templates/base.html`
- All nav links use `{% url 'name' %}` (never hardcoded paths).
- Nav order: `Home · Blog · Top 10 · Courses · Glossary · About · Contact`
- Active page uses `{% block nav_home %}` / `{% block nav_blog %}` etc, overridden as `text-gray-900 font-semibold`.
- When adding/removing nav items, edit `templates/base.html` and add/remove the corresponding nav block.
- The search bar and search toggle are built into `base.html` (inherited by all pages).

## Footer (`templates/base.html`)
- Brand description: `"Your hub for AI marketing insights, curated rankings, and free courses."`
- Logo dot: `text-red-600` (header and footer must match)
- Quick Links column: `Blog · Top 10 Listicles · Free Courses · Glossary`
- Important Pages column: `Privacy Policy · About Us · Contact`
- Contact column: email, response time, address
- No social icons in footer (social icons appear in sidebar widgets and contact page)

## Design system
- Background: `bg-[#faf8f5]`
- Accent (interactive elements): red (`text-red-600`, `hover:bg-red-600`)
- Card hover accent per section: red (blog), amber (Top 10 cards), indigo (course cards)
- Buttons with `aria-label` for icon-only elements: search, menu, social icons
- Title format: `Page — aimrarket`
- All `<img>` must have `width` + `height` attributes matching picsum URL dimensions
- Body metadata text: `text-gray-500` (not gray-400 — WCAG AA contrast)

## Git
- Branch: `main`
- `static/` is committed (required for pages to work — includes `output.css` and JS)
- `node_modules/` and `venv/` gitignored
