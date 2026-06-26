# aimrarket — AGENTS.md

## Quick start
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# CSS (optional — for Tailwind edits):
npm install          # installs tailwindcss + @tailwindcss/cli + @tailwindcss/typography
npm run dev          # watch: rebuilds static/css/output.css on change
npm run build        # one-time build (minified)
```

## Architecture
- **Django 5.2** project with 7 apps: `blog`, `glossary`, `top10s`, `courses`, `pages`, `search`, `api`
- **17 HTML templates** (base + 16 page templates + error pages), all extend `base.html` except `500.html`
- **2 non-HTML templates**: `robots.txt` (plain text), `glossary.md` (markdown export)
- **Tailwind CSS v4** via `@tailwindcss/cli` — no `tailwind.config.js`, no PostCSS
- Entry CSS: `src/input.css` — `@import "tailwindcss"` + `focus-visible` styles + `ckeditor-content` component styles
- Output: `static/css/output.css` — **committed** (served via `{% static %}`)
- All placeholder images from picsum.photos
- **REST API**: Django REST Framework with `DefaultRouter`, Token+Session auth, filter/search/order backends, page pagination (20/page)
- **Database**: SQLite, `CONN_MAX_AGE=60`, DatabaseCache backend (`django_cache` table)
- **Middleware**: SecurityMiddleware, GZipMiddleware, Session, Common, CSRF, Auth, Message, X-Frame-Options, custom `HtmlMinifyMiddleware`
- **Sitemaps**: 6 sitemap classes (StaticView, BlogPost, Course, Chapter, Profiles, GlossaryTerm) served via `sitemap.xml` index
- **Static files**: `static/` is source, `staticfiles/` is `collectstatic` output (both committed, `staticfiles/` gitignored)
- **All `<img>` must have `width` + `height` attributes matching picsum URL dimensions**

## Dependencies (requirements.txt)
- Django==5.2.15, djangorestframework==3.17.1, django-ckeditor==6.7.3, django-filter==25.2
- pillow==12.2.0, html2text==2025.4.15, sqlparse==0.5.5, tzdata==2026.2

## Apps

### `blog` — Blog posts
- **Models**: Category, Tag, Post (RichTextField body, status Draft/Published), UserComment (GenericForeignKey), Placeholder (shortcode system), FAQ
- **URLs**: `/blog/` → BlogHomeView (paginate_by=6), `/blog/<slug>/` → PostDetailView, `/blog/<slug>.md` → PostMarkdownView, `/blog/category/<slug>/` → CategoryView
- **Templates**: `blog/templates/blog/{post_list,post_detail,category}.html`
- **Custom tags**: `blog_extras.py` — `read_time`, `post_json_ld`, `faq_json_ld`
- **Admin**: PostAdmin with fieldsets, CategoryAdmin, TagAdmin, UserCommentAdmin, PlaceholderAdmin, FAQAdmin
- **Features**: Related posts (same category), reading progress bar, auto-generated TOC from ckeditor-content headings, FAQ accordion with JSON-LD, share buttons, markdown export

### `glossary` — AI Marketing Glossary
- **Models**: GlossaryTerm (term, RichTextField description, status Draft/Published), GlossaryPageConfig (SEO title/description)
- **URLs**: `/glossary/` → GlossaryIndexView, `/glossary.md` → GlossaryMarkdownView (project-level url)
- **Templates**: `glossary/templates/glossary/{index,glossary.md}.html`
- **Custom tags**: `glossary_extras.py` — `html_to_md`, `defined_term_set`
- **Admin**: GlossaryTermAdmin, GlossaryPageConfigAdmin
- **Features**: Letter-grouped terms (A-E, F-J, K-O, P-T, U-Z), cached 3600s with DatabaseCache, IntersectionObserver nav highlighting, copy-to-clipboard term links, debounced search filter, back-to-top, HTML→markdown export via html2text
- **Signals**: `clear_glossary_cache` — invalidates group cache on GlossaryTerm post_save/post_delete (connected in `glossary/apps.py:ready()`)
- **Middleware**: `HtmlMinifyMiddleware` — collapses whitespace in HTML responses

### `top10s` — Top 10 Listicles
- **Models**: Profiles (title, slug, RichTextField intro/tldr/conclusion, JSONField comparison_table), Tool (name, image, RichTextField description/pros/personal_review, ordered per listicle), PlaceholderProfile
- **URLs**: `/top10/` → ProfileListView (paginate_by=6), `/top10/<slug>/` → ProfileDetailView
- **Templates**: `templates/top10s/{profile_list,profile_detail}.html`
- **Admin**: ProfilesAdmin with ToolInline + PlaceholderProfileInline, ToolAdmin, PlaceholderProfileAdmin
- **Features**: Shortcode placeholder system, reading progress bar, comparison table, 10 tool cards with pros/cons and personal review

### `courses` — Free Courses
- **Models**: Course (title, slug, level Beginner/Intermediate/Advance, is_featured, RichTextField description/overview/objectives/requirements/about, image), Chapter (RichTextField content/summary, status draft/published, ordered via `number`), Practice (per chapter), ChecklistItem (per chapter)
- **Properties**: Course.lessons_count, Course.duration, Chapter.reading_time
- **URLs**: `/courses/` → CourseListView (`?level=` filter), `/courses/<slug>/` → CourseDetailView, `/courses/<slug>/<chapter_slug>/` → chapter_detail (function view with prev/next nav)
- **Templates**: `templates/courses/{course_list,course_detail,chapter_detail}.html`
- **Custom tags**: `course_extras.py` — `split`, `lines_to_list`
- **Admin**: CourseAdmin with ChapterInline, ChapterAdmin with PracticeInline + ChecklistItemInline, PracticeAdmin, ChecklistItemAdmin
- **Features**: Level filter pills (color-coded), syllabus with chapter list, prev/next lesson navigation, practice exercises, checklists, related courses

### `pages` — Static Pages
- **Views**: AboutView, PrivacyView (TemplateView), contact_view (function, ContactForm with Tailwind CSS classes)
- **URLs**: `/about/`, `/contact/`, `/privacy/`
- **Templates**: `templates/pages/{about,contact,privacy}.html`
- **ContactForm fields**: name, email, subject, message (Django Form, not stored — uses messages framework)

### `search` — Site Search
- **Views**: `search_view` (function, reads `?q=`)
- **URLs**: `/search/`
- **Template**: `templates/search/search.html`
- **Search scope**: Published Posts (title, short_answer, body, category name, tag names) + Profiles (title, intro, tldr, conclusion)

### `api` — REST API (DRF)
- **ViewSets** (all use `DefaultRouter`): GlossaryTermViewSet, GlossaryPageConfigViewSet, PostViewSet (different list/detail serializers), CategoryViewSet, TagViewSet, CourseViewSet, ChapterViewSet, ProfilesViewSet
- **Serializers**: `api/serializers.py` — GlossaryTerm(List), GlossaryPageConfig, Category, Tag, FAQ, Post(List/Detail), Practice, ChecklistItem, Chapter(List), Course(List/Detail), Tool, Profiles(List/Detail)
- **Endpoints**: `/api/glossary/terms/`, `/api/glossary/page-config/`, `/api/blog/posts/`, `/api/blog/categories/`, `/api/blog/tags/`, `/api/courses/`, `/api/chapters/`, `/api/top10s/`
- **Auth**: `rest_framework.authentication.TokenAuthentication` + SessionAuthentication
- **Permissions**: `rest_framework.permissions.IsAuthenticated` (global, read-only for unauthenticated where configured)
- **Filters**: DjangoFilterBackend, SearchFilter, OrderingFilter; PageNumberPagination (page_size=20)

## Template map
```
templates/
├── base.html               shared layout (nav, footer, search bar)
├── home.html               landing page
├── 404.html                404 error page
├── 500.html                standalone error page (no base.html)
├── robots.txt              allows all + sitemap link
├── pages/
│   ├── about.html          about us
│   ├── contact.html        contact form (Django Form, messages)
│   └── privacy.html        privacy policy
├── top10s/
│   ├── profile_list.html   Top 10 landing (cards + pagination + sidebar)
│   └── profile_detail.html single listicle (10 tools + comparison table)
├── courses/
│   ├── course_list.html    course catalog (level filter pills)
│   ├── course_detail.html  course detail + syllabus
│   └── chapter_detail.html single lesson (sidebar nav, practices, checklist)
├── search/
│   └── search.html         server-side search (reads ?q=)
└── (app-templates — inside each app's templates/ dir)
    ├── blog/templates/blog/
    │   ├── post_list.html    blog home (featured + grid + pagination + sidebar)
    │   ├── post_detail.html  single post (TOC, FAQ, share, related)
    │   └── category.html     category-filtered posts
    └── glossary/templates/glossary/
        ├── index.html        AI marketing glossary (letter groups, search filter)
        └── glossary.md       markdown export template
```

## Nav — shared via `templates/base.html`
- All nav links use `{% url 'name' %}` (never hardcoded paths).
- Nav order: `Home · Blog · Top 10 · Courses · Glossary · About · Contact`
- Active page uses `{% block nav_home %}` / `{% block nav_blog %}` etc, overridden as `text-gray-900 font-semibold`.
- When adding/removing nav items, edit `templates/base.html` and add/remove the corresponding nav block.
- The search bar and search toggle are built into `base.html` (inherited by all pages, toggled via `search-toggle.js`).

## Footer (`templates/base.html`)
- Brand description: `"Your hub for AI marketing insights, curated rankings, and free courses."`
- Logo dot: `text-red-600` (header and footer must match)
- Quick Links column: `Blog · Top 10 Listicles · Free Courses · Glossary`
- Important Pages column: `Privacy Policy · About Us · Contact`
- Contact column: email, response time, address
- Footer uses `<details>` for mobile accordion behavior
- No social icons in footer (social icons appear in sidebar widgets and contact page)

## Sitemaps (`aimrarket/sitemaps.py`)
- **StaticViewSitemap**: home, blog_home, profile_list, course_list, glossary_index, about, contact, privacy, search (priority 0.8)
- **BlogPostSitemap**: all published Post (priority 0.9)
- **CourseSitemap**: all Course (priority 0.7)
- **ChapterSitemap**: published Chapter (priority 0.6)
- **ProfilesSitemap**: all Profiles (priority 0.8)
- **GlossaryTermSitemap**: published GlossaryTerm (priority 0.6)
- Served via `/sitemap.xml` (index) and `/sitemap-<section>.xml`

## Design system
- Background: `bg-[#faf8f5]`
- Accent (interactive elements): red (`text-red-600`, `hover:bg-red-600`)
- Card hover accent per section: red (blog), amber (Top 10 cards), indigo (course cards)
- Buttons with `aria-label` for icon-only elements: search, menu, social icons
- Title format: `Page — aimrarket`
- Body metadata text: `text-gray-500` (not gray-400 — WCAG AA contrast)
- Base template has SEO block with Open Graph, Twitter Cards, JSON-LD-ready, canonicals, verification meta tags

## Static JS
- `static/js/search-toggle.js` — toggles search bar visibility (~300 bytes minified)
- `static/js/glossary.js` — debounced filter, IntersectionObserver nav, back-to-top, clipboard copy for term links
- `static/js/blog-post.js` — reading progress bar, auto TOC from `ckeditor-content` headings, copy-link button

## Admin
- **blog**: PostAdmin(fieldsets), CategoryAdmin, TagAdmin, UserCommentAdmin, PlaceholderAdmin, FAQAdmin
- **courses**: CourseAdmin(with ChapterInline), ChapterAdmin(with PracticeInline+ChecklistItemInline), PracticeAdmin, ChecklistItemAdmin
- **glossary**: GlossaryTermAdmin, GlossaryPageConfigAdmin
- **top10s**: ProfilesAdmin(with ToolInline+PlaceholderProfileInline), ToolAdmin, PlaceholderProfileAdmin
- **pages/search/api**: No models registered for admin

## Git
- Branch: `main`
- `static/` is committed (required for pages to work — includes `output.css` and JS)
- `.gitignore` ignores: `node_modules/`, `venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `db.sqlite3`, `staticfiles/`, `dist/`
