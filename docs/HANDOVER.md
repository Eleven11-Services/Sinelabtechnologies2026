# Handover: Sinelab Technologies website

State as of **2 November 2026**. The previous Claude (Cowork) sessions built everything in `site/` and wrote this file when the project moved to Claude Code. The raw day-by-day log is in `history-notes.md`. Its file paths point to the old cloud workspace and no longer exist.

## 1. Where things stand

| | |
|---|---|
| Pages | All six are built and reviewed by the user: Home, About Us, Solutions, Projects, Gallery, Contact |
| User approval | Homepage approved ("final approval", 23 Oct). Later rounds approved section by section through comments |
| Client approval | **Pending.** The user said to wait for Sinelab's approval before the real launch |
| Checks | `npm run check`: 0 axe violations, no console errors and no broken images on all pages, desktop and phone (2 Nov) |
| Search engines | All pages carry `noindex, nofollow` because the build still contains sample content. Remove this at launch |

### Hosting

- **Vercel:** `sinelab-website.vercel.app`, Vercel account/team `pooja-5b72`, GitHub repo `poojaguneshuiux/sinelab-website`.
  - The user uploads to GitHub themselves; Claude has no access.
  - The user asked to "push to production". Check with them whether the latest build (the folder `Downloads\sinelab-website-vercel-v2` on their PC, identical to `site/` here) has actually been uploaded.
- **Netlify:** `sinelabtest.netlify.app`, an older review deploy (26–29 Oct build) that uses Netlify Forms. Form notifications go to info@sinelabtechnologies.com.
- **Review artifacts on claude.ai** (the user can open these; Claude Code cannot):
  - draft: https://claude.ai/artifact/9RiaKn4eWfiFizxFp1vVCU
  - old approved homepage v48: https://claude.ai/artifact/RRv8ty8hEjUCvunRpwdTfQ

## 2. Content facts (use exactly)

- Company: **Sinelab Technologies Pvt. Ltd.** Industrial heritage since 1996 (Kanjikode).
  - Tagline: **"Powering Your Tomorrow"**, used in the footer on all pages and in the homepage hero.
  - Voice: confident, human, engineering-led, credible.
- Phone and WhatsApp: **+91 99462 07738** (`tel:+919946207738`, `https://wa.me/919946207738`). Email: **info@sinelabtechnologies.com**.
- Offices:
  - **Palakkad:** Sinelab Technologies Pvt Ltd, Prathiba Nagar, Chandranagar Colony, Palakkad, Kerala 678007. Google place_id `ChIJDznElBNtqDsRwlGeDS40paQ`.
  - **Kochi:** Sinelab Solar, Mahakavi Vailoppilli Rd, Ponnurunni, Vyttila, Kochi, Kerala 682032. Google place_id `ChIJcaY_7vENCDsRLxtGqYodVqE`.
  - Hours "Mon–Sat 9:00 am–5:30 pm" come from the Google listings and are not yet confirmed by the client.
  - The contact map is a drawn SVG of central Kerala (coastline from Natural Earth, public domain) with both pins linked to Google Maps. A Google embed was dropped because the review preview blocked it.

### Team

The About page shows everyone. The homepage shows Sajeev, Sunil and Athul.

| Name | Role | Tag | Notes |
|---|---|---|---|
| Sajeev Kumar K | Managing Director | Co-founder | Large card with bio |
| Sunil Joseph | Director | Co-founder | Large card with bio |
| Athul S. Krishna | Chief Marketing Officer | Leadership | Name and role only |
| Sravan Paul Sunil | Chief Operating Officer | Leadership | Name and role only |
| Ravinder Mehta | Head of Solar Division | Leadership | Name and role only |
| Saran | Regional Manager, Kochi Division | Team | Division on a second line |
| Leenu Joseph | Project Engineer, Kochi Division | Team | Division on a second line |

- The leader messages on the homepage are drafted from the bios and tagged "Draft quote · for approval". Each person must approve or rewrite theirs before launch.
- The homepage team button links to `about.html#ab-team`.

### Projects

These are real drone photos and are the only projects shown.

| Order on Projects page | Key | Sector / type | Capacity in the file name (NOT shown) |
|---|---|---|---|
| 1 Bava Metals | bava | Commercial building / rooftop | 35 kWp |
| 2 Grand Bajaj Showroom | bajaj | Vehicle showroom / rooftop | 70 kWp |
| 3 Bala Cinemas | bala | Cinema / rooftop, Enphase microinverters | 70 kWp (content doc says 170 kW: **conflict**) |
| 4 Jamal Sons | jamal | Commercial building / rooftop | 30 kWp |
| 5 Palakkad Surgicals | psurg | Manufacturing / rooftop | 30 kWp |
| 6 Sinicon | sinicon | Industrial / rooftop | 70 kWp |
| 7 Salim Hybrid Residence | salim | Residential / hybrid solar | (content doc "Saleem Residence", 20 kW) |

- The project data lives in `const PROJECTS = [...]` in `projects.html`, and the case-study dialog is built from it.
- Capacities stay hidden until the client confirms them. That was the user's choice.
- **Homepage "Featured projects"** (changed 3 Nov at the user's request: "avoid the scroll to see projects… just 3–4 then a CTA"):
  - The old pinned sideways slider is gone. The section is now a one-glance grid (`#projGrid`): Bava Metals as the large card, then Grand Bajaj, Salim Hybrid Residence and Bala Cinemas, then a dark "View all 7 projects" card. That card shows round photos of Jamal Sons, Palakkad Surgicals and Sinicon and links to `projects.html`.
  - Layouts: desktop is one large card plus a 2×2 block; tablet puts the large card on top, three in a row and the "View all" bar below; phones show the large card, then a compact list, then the button.
  - On short laptop screens the small photos get shallower (`max-height` tied to `100svh`), so all four stay in view.
  - The order (Salim 3rd) is the user's choice.
- Homepage "Projects in motion" films are 3 s clips each and auto-advance: **Pyarelal 1 MW rooftop** (`mw1`), **Palakkad Surgicals** (`psurg`), **Sinicon** (`sinicon`). They are slow push-ins rendered from still photos until real drone video arrives (see `tools/make_film.py`).
- Gallery highlight deck (top of `gallery.html`): Bala, Bajaj, Bava, Salim, Palakkad Surgicals, Sinicon. Salim replaced Jamal there at the user's request. Data is in `const HIGHLIGHTS`; grid data is in `const GALLERY`.
- The gallery grid has a "Sinelab projects" row of real photos, then a "Sample photos" masonry. Every tile in it is labelled, and a note says they are placeholders.

### Other content

- The savings calculator assumptions are in `const CALC` in `index.html`: tariffs, ₹/kW, the PM Surya Ghar subsidy formula and the CO₂ factor. Get the client to confirm them before launch.
- About › Recognition: the 2018 Asianet Keerthimudra award card uses a drawn emblem, with "Award photo to be added".
- About › Manufacturing site cards: Kanjikode 1996, Thodupuzha 2002, Coimbatore 2008, Qatar, Kanjikode Industrial Area 2024. To verify: award name and year, the SARK Cables spelling, Thodupuzha details and the Qatar entity.

## 3. What the user likes and dislikes

- **Likes:** premium, calm motion; real photos; editorial layouts; one clear idea per section; things that work well on phones.
- **Rejected in the past:**
  - a "creative pass" with heavy effects (only the "Why Sinelab" section survived)
  - a childish floating solar-panel icon and its replacements
  - a scroll-driven About hero and the "Powered by progress" line
  - a yellow CTA band
  - a six-in-a-row team layout ("not nice")
  - a 3D card flip in the gallery (they wanted a sideways slide)
  - the brand-guidelines-driven redesign ("we don't need this")
- **Comment style:** short comments on a specific section, for example "feels congested", "make it mobile friendly" or "pls add some background elements, it feels so gap". Read the intent, make the smallest change that fixes it, and show a screenshot.

## 4. Technical decisions worth knowing

- **No build step.** The site was originally generated by Python scripts that stitched one homepage source with page modules and patches (`docs/legacy-build/`). Those scripts depend on files that no longer exist. **`site/` is now the source of truth**, so edit the HTML directly.
- **Shared blocks are duplicated in every page:** nav, menu, footer, WhatsApp button, core script, tokens and base CSS. See CLAUDE.md for how to change them safely. A worthwhile refactor, once the client has approved, would be to move the shared CSS and JS into `assets/css/site.css` and `assets/js/site.js`. Do it only with the user's OK, and confirm with `npm run check` and screenshots that nothing changed visually.
- **Performance work (29 Oct, the user said the site was lagging):**
  - all images converted to WebP (13.4 MB → 8 MB)
  - 3D pixel ratio capped and a cheaper shadow map
  - phones use native scroll instead of Lenis touch
  - no backdrop blur on the sample labels
  - homepage first load is about 2.7 MB
- **Page-switch scroll fix (29 Oct):** after the user scrolled to the bottom and changed pages, the new page opened at the bottom. The fix is in the core script on every page (see CLAUDE.md).
- **Hero image clean-up (2 Nov):** the old wide hero mirrored and blurred the photo at the sides, which made the trees look doubled. It was rebuilt without mirroring:
  - a clean sky gradient
  - real leafy tree edges borrowed from the photo's own crown
  - hedges and lawn continued from real texture
  - the alpha layers were rebuilt with sky holes inside the crowns and edge-colour decontamination, so there is no pale halo at dusk or night

  The sources are `assets-source/hero/`, and the scripts are in `docs/legacy-build/hero/` for reference. AI outpainting (LaMa) was tried and rejected because it smeared.
- **Typeface: Manrope (5 Nov).** No brand font was ever supplied, and the site first used Inter Tight as a close match. The user then asked whether the logo was Inter, so the wordmark was tested against 11 fonts by overlaying the shapes.
  - Manrope matched almost exactly (light "Sine", medium "lab", tight tracking), so the logo is very likely set in Manrope. Inter Tight was next. DM Sans was weaker and has no tabular figures.
  - The whole site now uses Manrope, which has tabular figures and the ₹ sign. **Approved by the user on 5 Nov.**
  - Re-checked in Claude Code (5 Nov): overlaid on `logo-black-web.png` with the dotless ı, Manrope (Sine 300, lab 500) covers 83% of the wordmark shape and Inter Tight 75%. The S terminals, the e bar and the a bowl follow Manrope.
  - The brand guidelines PDF in `docs/reference` still says Inter Tight. Update it at its next revision, and confirm the font with Sinelab's logo designer if possible.
- **Forms:** FormSubmit on Vercel, which needs the one-time activation click; Netlify Forms on the older Netlify build.
- **Team photos** were cropped with face detection to square (About) and 3:4 (homepage). Founder photos use `object-position:50% 12%` on phones so heads aren't cut off.

## 5. Assumptions to confirm with the user or client

1. The 1 MW milestone photo is labelled **Pyarelal**, the content doc's only 1 MW rooftop. This is an assumption.
2. Photo matching: Sajeev = older man with glasses in a navy blazer; Sravan = young man in a grey blazer on white; Ravinder = grey beard, denim shirt, blue backdrop. Sunil, Athul, Saran and Leenu are certain.
3. The hero says "Powering **Your** Tomorrow". Revert to "Powering Tomorrow" if the client prefers.
4. The "Reasons to choose us" heading became "About us", and the intro label also says "About us". Flag this if the client minds.

## 6. Open items

**Needed from the client**

- [ ] Capacities for all seven projects (Bala: 70 vs 170 kW)
- [ ] Locations and status for the projects
- [ ] Drone videos to replace the three still-photo clips. If they have sound, they need captions
- [ ] Award photo (2018 Asianet Keerthimudra)
- [ ] Vector logo (SVG)
- [ ] More real gallery photos: manufacturing (battery assembly, inverter testing, lighting production, Kanjikode facility), people (crew, commissioning, engineers) and milestones
- [ ] Approved testimonials (the `#reviews` section stays hidden until then)
- [ ] Each leader approves or rewrites their quote
- [ ] Office hours (social links done 5 Nov: Instagram and Facebook only)
- [ ] Privacy Policy and Terms text (the content doc has drafting briefs; needs legal review)

**Site work before launch**

- [x] Clean-up: unused `inter-tight-*.woff2` and `real_*_slide.webp` removed (done 3–5 Nov).
- [ ] Replace or label the remaining sample images on the homepage. `about.webp` in the About intro and the three blog cards (`blog1–3.webp`) are sample photos with no "Sample photo" label. The blog itself is sample content. Either label them, swap in real photos, or hide the blog until real articles exist. Ask the user which.
- [ ] Add the Privacy and Terms pages, and point the footer links at them (they currently go to `index.html`)
- [x] Social links in the footer: Instagram and Facebook (5 Nov); LinkedIn removed
- [ ] Remove `noindex` on all six pages
- [ ] FormSubmit activation, plus a test submission from both forms
- [ ] Decide on a visible pause control for auto-advancing carousels and floating icons (WCAG 2.2.2)
- [ ] Domain: keep the MX records when pointing DNS at Vercel. Vercel Hobby is non-commercial, so plan for Pro

## 7. Working with the user

- The user is Pixel (Team E11 / Eleven:11 Services), building this for the client Sinelab.
- Messages are short and informal. Replies should be short too: say what changed and where, and show a screenshot.
- Always ask before deploying or publishing anything, and say how to roll it back.
- They will upload to GitHub and Vercel themselves. Give click-by-click steps, never ask for credentials, and remember the GitHub web uploader takes at most 100 files per upload.
