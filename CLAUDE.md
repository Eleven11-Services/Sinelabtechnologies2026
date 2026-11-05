# Sinelab Technologies website

Marketing site for **Sinelab Technologies Pvt. Ltd.**, a Kerala company (Palakkad and Kochi) that has made industrial products since 1996 and now delivers solar, energy storage and lighting. The site is static, hand-written HTML, CSS and JS with no framework and no build step. What is in `site/` is exactly what gets deployed.

The full history of decisions is in `docs/HANDOVER.md`. Read it before you make design changes.

## Rules that always apply

1. **Get approval before anything goes live, and keep a way back.** Show the user the change first, using screenshots, a local preview or a branch. Push to production only after they say yes. Each deploy must be revertible: commit before you change anything, and the Vercel instant rollback is described below. The client (Sinelab) also has to approve before launch.
2. **Never ask for, accept or use passwords, tokens or API keys.** Do not sign in to GitHub, Vercel, Netlify or Google for the user. The user does uploads and dashboard settings themselves. Give them exact steps instead.
3. **WCAG 2.2 AA on everything.** This applies to this site and to every other project. `npm run check` must report 0 axe violations on desktop and phone before you hand anything back. The house rules are listed below. The `wcag-accessibility-expert` skill covers the rest; use it for any UI work. It lives in `.claude/skills/wcag-accessibility-expert/SKILL.md`. If that folder is missing, copy `docs/reference/WCAG_Accessibility_Expert_Skill.md` there, or read that file directly.
4. **Do not present anything as real when it isn't.**
   - Stock or sample photos carry a visible `<span class="hl-ph">Sample photo</span>` label.
   - Leader quotes carry a "Draft quote · for approval" tag until each person approves them.
   - Placeholder testimonials stay hidden.
   - Capacities are hidden until the client confirms them.
5. **Brand.**
   - Colours are black, white and Sinelab yellow `#F9C22E`. Yellow is never used as text on white; use `--accent-ink #806000` instead.
   - The only typeface is **Manrope**, self-hosted. It is the typeface of the Sinelab wordmark: light "Sine", medium "lab", tight letter spacing. The switch from Inter Tight was made on 5 Nov 2026.
   - The site should feel premium and engineered, with subtle motion. The user dislikes anything that looks AI-made, childish or busy, so avoid heavy effects, gradients-for-show and emoji.
6. The user reviews visually and section by section. Make one change at a time, then show a screenshot of it.

## Layout

```
site/                  the deployable website (Vercel "Root Directory" = site)
  index.html           homepage
  about.html  solutions.html  projects.html  gallery.html  contact.html
  assets/img/          all images (WebP, plus og.jpg and apple-touch-icon.png)
  assets/js/           gsap 3.12.5, ScrollTrigger, lenis 1.1.13, three r128 (self-hosted, no CDNs)
  assets/fonts/        Manrope woff2 (300–700, latin + latin-ext)
  media/               homepage "Projects in motion" clips (.mp4 + .webm)
  vercel.json          cache + security headers
  favicon.png
assets-source/         full-size originals (not deployed)
  brand/               client brand pack + guidelines PDF + web logos
  photos/projects/     real project drone photos (jpg, ≤4000 px)
  photos/team/         team portraits
  hero/                original hero house photo + cleaned wide scene
tools/                 check.js, screenshots.js, to_webp.py, make_film.py
docs/HANDOVER.md       history, decisions, content facts, open items  ← read this
docs/history-notes.md  raw working log from the previous sessions
docs/reference/        client content master doc, requirements PDF, WCAG skill
docs/legacy-build/     old Python generators (reference only, do not run)
.claude/skills/        wcag-accessibility-expert skill (copy of docs/reference/WCAG_Accessibility_Expert_Skill.md)
```

## How the pages are put together

- Every page is **one self-contained HTML file**, with all of its CSS in `<style>` in the head and all of its JS in `<script>` at the end of the body. There are no shared .css or .js files apart from the libraries.
- **Shared blocks are copied into all six pages.** Each page carries its own copy of:
  - the `:root` tokens and the base CSS (each subpage also includes the homepage CSS)
  - the nav (`<!-- ======= NAV ======= -->`, `.nav`) and the phone menu (`#mnav`, `#mnavScrim`, `#menuBtn`)
  - the footer (`<footer class="band">`)
  - the WhatsApp button (`<aside aria-label="WhatsApp chat">`)
  - the core script: open-at-top scroll fix, Lenis, mobile menu, glass nav, floating elements, reveal

  These copies are *near* duplicates. The nav uses `aria-current="page"` per page, the homepage links to its own `#sections`, and subpages link to `index.html#…`. So when you change a shared block, make the change in all six files and diff the results (`grep -c` the new string in each file). Do not paste one page's block over another's.
- Inside each file, sections are marked with `<!-- ======= NAME ======= -->` and their CSS and JS with `/* ---------- Name ---------- */`. Search for those markers to find a section.
- Homepage section ids, in order: `hero`, `about`, `films`, `why`, `anatomy` (on-grid / off-grid / hybrid 3D model), `solutions`, `savings` (calculator), `projects`, `team`, `reviews` (hidden), `gallery`, `faq`, `blog` (sample guides), `contact`.
- Section ids on the other pages:
  - About: `ab-hero`, `story`, `recognition`, `milestones`, `vision`, `facilities`, `ab-team`, `cta`.
  - Solutions: `sl-hero`, `services` (with `#residential`, `#commercial`, `#storage`, `#lighting` …), `compare`, `process`, `sl-faq`, `cta`.
  - Projects: `pj-hero`, `work`, `cta`.
  - Gallery: `gl-hero`, `photos`, `cta`.
  - Contact: `ct-hero`, `enquiry`, `offices`.
- `data-g="…jpg"` attributes in gallery.html are lookup keys that let the highlight deck reuse grid images. They are not file paths.

### Tokens (in `:root` on every page)

```
--sun:#F9C22E  --accent-ink:#806000  --ink:#09090B  --navy-deep:#09090B  --slate:#66666E
--paper:#F4F4F5  --muted:#5F5F69  --line:#E4E4E7  --on-dark-muted:#A1A1AA
--f-display / --f-body / --f-mono: all "Manrope", "Helvetica Neue", Arial, sans-serif
```

### Motion conventions

- GSAP + ScrollTrigger for scroll effects. Lenis smooth scroll runs on desktop only; phones use native touch scroll (`syncTouch` is off).
- Every page opens at the top: `history.scrollRestoration='manual'` plus `ScrollTrigger.clearScrollMemory('manual')`, then a scroll to 0 at start, after Lenis init, on load and on bfcache `pageshow`. Links that carry a `#hash` still land on their section. Keep this behaviour.
- `prefers-reduced-motion: reduce` must show everything static: no pinning, no auto-advance, all content visible. Test new motion with reduced motion on (check.js does this).
- The homepage hero is a 2410×1196 layered scene. Scrolling moves it from day to dusk to night.
  - Photo layers: `day.webp`; `fg_day`, `fg_dusk` and `fg_night` (alpha cut-outs of the house and trees); `win0–8` and `lamp0–1` (screen-blended lights); `panels.webp` (mask for the glint); `stars.webp`.
  - The sky colours are CSS gradients, not images.
  - If you edit the scene, keep the layer sizes and positions identical. The source images are in `assets-source/hero/`.
- The 3D model (`#anatomy`) is Three.js r128. Its pixel ratio is capped at 1.5 on desktop and 1.25 on phones, with a 1024 PCF shadow map. Keep these caps for performance.

## Accessibility house rules (already in place, keep them)

- Two-tone focus ring (ink outline + yellow halo) on every interactive element. `scroll-padding-top:110px` keeps focused items clear of the floating nav (2.4.11).
- Targets are at least 24×24 px. WhatsApp green is `#128748` for contrast.
- Dialogs (`projects.html` case studies, gallery viewer) are native `<dialog>`. They trap focus, close on Esc, the backdrop and ×, and return focus to the opener.
- Forms:
  - inline errors use `aria-invalid` + `aria-describedby`
  - an error summary uses `role=alert`, and focus moves to the first error
  - success uses `role=status` and focus moves to it
  - a honeypot field is included
- Filters use `aria-pressed` and a live count. Decorative SVG and images use `aria-hidden` or `alt=""`.
- Footer column headings are `h3`. Keep one `h1` per page and a logical heading order.
- Open question: a visible pause control for auto-advancing carousels and the floating icons (2.2.2).

## Images and media

- Everything served is WebP: photos q72 with a longest side of 1920; cards, portraits and thumbs 1200; video posters 1280. Every `<img>` has `decoding="async"`, and below-the-fold images also have `loading="lazy"`. `og.jpg` is 1200×630.
- Naming:
  - `real_<key>.webp` (full), `real_<key>_card.webp` (5:4, Projects page)
  - homepage Featured projects: `real_bava_feat.webp` (large card), `real_<key>_tile.webp` (16:10, 1000 px), `real_<key>_dot.webp` (160 px circles on the "View all" card)
  - `team_<key>_sq.webp` (square, About page), `team_<key>_tall.webp` (3:4, homepage)
  - `film_<key>.webp` and `film_<key>_t.webp` (clip poster and tab thumb)
- Project keys: `bava`, `bajaj`, `bala`, `jamal`, `psurg` (Palakkad Surgicals), `sinicon`, `salim`; film keys: `mw1`, `psurg`, `sinicon`.
- Convert new photos with `python3 tools/to_webp.py <src> -o site/assets/img/<name>.webp [--max 1200] [--crop 5:4] [--focus 0.5,0.4]` (needs Pillow). Put the original in `assets-source/`.
- For a homepage clip from a still photo, run `python3 tools/make_film.py <photo> <key> --focus x,y --zoom 1.12 --seconds 3` (needs ffmpeg). The docstring explains how to cut a real drone video instead.

## Forms

- Both forms (homepage `#contact` and the contact page) post with `fetch` to FormSubmit: `https://formsubmit.co/ajax/info@sinelabtechnologies.com`. The hidden fields are `_subject`, `_template=table`, `_captcha=false` and `_honey`.
- FormSubmit sends **a one-time activation email** to info@sinelabtechnologies.com on the first real submission. Someone at Sinelab must click it, or nothing gets delivered.
- If sending fails, the page shows "call or WhatsApp us".
- Netlify alternative: an older build used Netlify Forms (`data-netlify="true"`, `form-name` = `homepage-enquiry` / `enquiry`). Use that only if hosting moves back to Netlify, and replace `vercel.json` with a `_headers` file.

## Commands

```
npm install                      # playwright + axe-core (dev only)
npx playwright install chromium  # once
npm run serve                    # http://localhost:8000 (tools/serve.js, plain Node)
npm run check                    # all pages × desktop/phone: console errors, 404s, broken images,
                                 # unexpected external requests, axe WCAG 2.2 AA. Must end "All pages clean".
node tools/check.js about.html   # one page
npm run screenshots              # full-page PNGs → screenshots/ (git-ignored); --viewport for first screen only
```

Before you report back after any change, run `npm run check`. Then take screenshots of the pages you touched at desktop and phone width, and look at them.

## Deploying (the user does the uploads)

- Hosting is Vercel, connected to a GitHub repo. The recommended setup is to push this whole folder to the repo and set **Vercel → Project → Settings → Build & Deployment → Root Directory = `site`**, with framework preset "Other", no build command and no output directory.
  - An older repo had the site files at its root. If that repo is still used as-is, upload only the contents of `site/`.
- Flow: commit → push to a branch → Vercel preview URL → the user and client approve → merge to main (production).
- **Rollback:** Vercel → Deployments → pick the previous production deployment → "Instant Rollback" / "Promote to Production", or `git revert`.
- Vercel's Hobby plan is for non-commercial use, so a Pro plan is needed for the company's live site.
- **At launch, on the real domain:**
  - remove `<meta name="robots" content="noindex, nofollow">` (and the comment above it) from all six pages
  - add the Privacy Policy and Terms pages; the footer links currently point to `index.html`
  - fill in the social URLs in the footer, which also point to `index.html` for now
  - keep the existing MX records when changing DNS
  - do a test submission of each form

## Open items

Open items are listed in `docs/HANDOVER.md` → "Open items". Do not invent anything that is still pending: capacities, quotes, testimonials, addresses, opening hours or awards.
