# aimrarket — AGENTS.md

## Quick start
```bash
npm install          # installs tailwindcss + @tailwindcss/cli
npm run dev          # watch: rebuilds dist/output.css on change
npm run build        # one-time build
npm run dev &        # keep running in background while editing HTML
```

## Architecture
- **11 static HTML pages**, no framework, no backend
- **Tailwind CSS v4** via `@tailwindcss/cli` — no `tailwind.config.js`, no PostCSS
- Entry CSS: `src/input.css` — only `@import "tailwindcss"` + global `focus-visible` styles
- Output: `dist/output.css` — **committed** (pages reference it directly)
- All images from picsum.photos placeholder service

## File map
```
index.html              landing page (hero + blog/top10/courses previews)
bloghome.html           blog home (category pills + post grid + sidebar)
post.html               single blog post
category.html           category-filtered posts
top10index.html         Top 10 landing (listicle cards)
top10-ai-tools.html     detailed Top 10 listicle (10 items)
courses.html            course catalog (8 courses, level filter)
course-chatgpt-marketers.html  single course detail (syllabus)
about.html              about us (story, values, 2 team members)
contact.html            contact form
search.html             client-side search (reads ?q= parameter)
```

## Nav — shared across all 11 pages
When adding/removing nav items, update ALL 11 HTML files:
`index.html`, `bloghome.html`, `post.html`, `category.html`, `top10index.html`, `top10-ai-tools.html`, `courses.html`, `course-chatgpt-marketers.html`, `search.html`, `about.html`, `contact.html`

Nav order: `Home · Blog · Top 10 · Courses · About · Contact`

Active page uses `class="text-gray-900 font-semibold"` on the nav `<a>`.

## Search bar boilerplate
Every page must include after `</header>`:
```html
<div id="search-bar" class="hidden bg-white border-b border-gray-200 shadow-sm">...</div>
```
And the search toggle script before `</body>`:
```html
<script>(function(){...})()</script>
```
Copy-paste the exact implementation from index.html lines 34–52 and 212–218.

## Footer
- Brand description: `"Your hub for AI marketing insights, curated rankings, and free courses."`
- Logo dot: `text-red-600` (header and footer must match)
- Social hover: all `hover:bg-red-600`
- Quick Links column: `Blog · Top 10 Listicles · Free Courses · About`
- Popular column: latest 3 popular content items

## Design system
- Background: `bg-[#faf8f5]`
- Accent (interactive elements): red (`text-red-600`, `hover:bg-red-600`)
- Card hover accent per section: red (blog), amber (Top 10 cards), indigo (course cards)
- Buttons with `aria-label` for icon-only elements: search, menu, social icons
- Title format: `Page — aimrarket`
- All `<img>` must have `width` + `height` attributes matching picsum URL dimensions (prevents CLS)
- Body metadata text: `text-gray-500` (not gray-400 — WCAG AA contrast)

## Git
- Branch: `main`
- `dist/` is committed (required for pages to work)
- `node_modules/` gitignored
