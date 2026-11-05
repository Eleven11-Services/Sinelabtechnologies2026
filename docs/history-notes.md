# History notes (raw working log)

> Copied unchanged from the Cowork sessions (22 Oct – 5 Nov 2026). It is a chronological log, so later entries override earlier ones.
> Paths like `/tmp/claude-0/...`, `src_draft.html`, `systems2.py` or "draft v54" refer to the old cloud workspace and review artifact. They do not exist in this repo.
> The current state is summarised in `HANDOVER.md`, and `site/` is the source of truth.

---

# Sinelab Technologies website: working notes

Approved preview (artifact): https://claude.ai/artifact/RRv8ty8hEjUCvunRpwdTfQ (Version 48)
Draft artifact: https://claude.ai/artifact/9RiaKn4eWfiFizxFp1vVCU (v18 = approved homepage + about.html (approved) + solutions.html (AWAITING REVIEW))
Content source: "Sinelab Website Content Master Document" (draft for approval, Oct 2026), supplied by the client.
Client meeting talking points: claude/sinelab-client-pitch-notes.md (still describes Panel anatomy; update if the draft is approved).

## Accessibility rule from the user (23 Oct 2026)
Follow WCAG 2.2 AA on everything (all projects, not just this one). The A11y Enforcer plugin is installed for that. Check with its scan + contrast scripts and an axe-core run (/tmp/claude-0/site/axe.js; axe-core in /tmp/claude-0/axe). Draft v8: 0 axe violations on desktop and phone.
v8 fixes: --slate #66666E; dark-menu numbers #A1A1AA; WhatsApp green #128748 inside an <aside>; two-tone focus ring (ink outline + yellow halo); visible focus on the bill input and Firefox range thumb; footer h4→h3; project track focusable region; scroll-padding-top 110px; form error message (role=alert, aria-invalid, aria-describedby) and role=status success; menu moves focus to the first link; lang fallback.
Still to decide: a visible pause control for the gallery auto-advance and floating icons (2.2.2); captions only needed if real drone videos have sound.

## Working rule from the user (22 Oct 2026)
Get the user's approval before anything goes live, and always keep a way to revert. Big changes go to the draft artifact first; the approved artifact stays untouched until the user says yes.

## Brief
- Client: Sinelab Technologies Pvt. Ltd. Custom native HTML/CSS/JS.
- Positioning: Kerala-rooted engineering and manufacturing company with an industrial heritage dating to 1996, delivering solar, energy storage, lighting and related energy solutions. Voice: confident, human, engineering-led, premium, credible.
- Colours: black, white, Sinelab yellow #F9C22E (accent ink #806000). Font: Inter Tight only.
- User wants the site to not feel AI-made; dislikes heavy/childish effects; judges changes section by section, mostly via artifact comments. Comment watches can't register from this remote session, so the user says "done" and Claude reads the comments.

## Draft v4 (23 Oct) – on-grid / off-grid / hybrid (client request, replaces Panel anatomy)
- Same pinned layout as the old anatomy section (id #anatomy kept for the dark-nav logic; class .systems). Heading "On-grid, off-grid or hybrid?", three list items (copy + "Best for…" line), CTA "Not sure which fits? Ask an engineer" → #contact.
- Three.js maquette on a dark plinth: two-volume flat-roof house, 2×5 tilted panel array, inverter + display on annex wall, net meter, battery bank with 5-step charge gauge, grid pole with two overhead lines.
- Scroll (+=330%): 3 steps × (midday → after sunset). Yellow dots = solar/battery power, white = grid power, along cable tubes; battery and pole/meter rise or sink per system; windows glow amber at night; clock pill shows time + solar kW; tag follows the active part (net meter / grid / battery % / hybrid inverter).
- Phones: model runs edge to edge, camera fitted to stage aspect, legend + CTA hidden. Reduced motion: no pin, hybrid shown, all three descriptions open.
- Also fixes the browser's default 8px body margin (html,body{margin:0}), which the live build had.
- v5 (user: "more realistic and premium"): Kerala villa (two storeys, timber louvres, sunshade, sit-out, wood door), raised GI panel frame, water tank, lawn + stone path + compound wall with gate lamps, two coconut palms, KSEB concrete pole outside the wall, soft contact shadows, unlit ground that fades into the page, warm night lighting, light pulses inside the cables instead of dots.
- Logo (v11, user): on light backgrounds the nav logo is black instead of navy blue (logo_black.png, made from logo.png: blue wordmark → #09090B, bluish tagline → neutral grey, yellow mark unchanged); white logo stays on dark sections. Placeholder {{LOGO_BLACK}} handled in build.py, build_draft.py and deploy.py (→ assets/img/logo-black.png).
- Our people (v12, from the user's screen recording – copy layout + animation only): three tall portrait cards in one row; hover/tap/focus widens a card (flex-grow 1.6), photo scales 1.06, message rises above the name (uppercase name, yellow role, dark bottom fade). Message replaces the reference's social icons (no social links supplied). Phones: swipeable snap row, messages always shown; Lenis ignores .leaders on phones. Backup of the previous team code: systems2_v11.py.
- Our people (v10, superseded): horizontal cards on a grey panel – portrait left; name, role, divider, message right; two on the first line, third centred; stacked on tablets/phones.
- Leader messages (v7): drafted from the bios, each tagged "Draft quote · for approval" – each leader must approve or rewrite before launch.
- Our people (v6, user: "two in one line, 3rd in center, just photo and name title"): portrait cards, MD + Director on the first line, CMO centred below; name then role only. Circuit drawing and bus lines removed. (A role/name/quote row version came first, v5, and was replaced.)
- Solutions (v6): descriptions removed from all 8 cards (tag, title, icon only); phone accordion + chevrons removed, now a plain list.
- Build: systems.py (reads src_v48.html → src_draft.html), then systems2.py (team + realistic model), then build_draft.py → sinelab-draft.html. On approval: copy src_draft.html → src.html, build.py, publish main, deploy.py.

## Approved version (v48)
- Smooth scroll: Lenis on wheel AND touch (syncTouch), ScrollTrigger ignoreMobileResize.
- Mobile menu: glass dropdown under the nav pill, staggered links 01–06, hamburger→X, scrim, scroll locked.
- Nav: floating liquid-glass pill, compacts with jelly squash, dark glass over dark sections.
- About facts strip: journey line, dots light in sequence, digits roll like a meter. Phones: 2×2, no line.
- Why Sinelab: sticky heading (no underline), ring stage with moving sun; reasons light up at screen centre.
- Featured projects (desktop): pinned, one stop per project with eased glide (.pj-steps / .cur). Phones: swipe.
- Others: hero day→night, films (sample clips), panel anatomy (3D), solutions (phone accordion), calculator, our people, testimonials hidden, gallery panels, FAQs, blog, contact, footer, floating solar icons.

## Rejected so far
Creative pass (22 Oct): only the Why section was kept. Brand guidelines PDF + asset ZIP (21 Oct): "we don't need this". Childish floating solar-panel icon and its sun-glow/sine/grid replacement. About page: scroll-driven hero and the "Powered by progress" line (v15); yellow CTA band (v16).

## Build files (session-only, /tmp/claude-0/site)
src.html (approved v48, backup src_v48.html) · src_draft.html (draft) · build.py → sinelab-home.html · deploy.py → /tmp/claude-0/deploy/sinelab-website.

## Plan (23 Oct, user)
Do NOT upload to Netlify until ALL pages are complete. Homepage is done (awaiting client comments). Remaining pages per the content doc's navigation: About Us (approved), Solutions (in review), Projects (in review), Gallery (in review), Our People, Contact (plus legal pages in the footer). deploy.py must be extended for multi-page (about.html etc.) before the hand-over.

## About Us page (23 Oct, draft v17 – awaiting review)
Published inside the draft artifact as a second file, about.html (open "About Us" in the nav, or Discover our story). Built by /tmp/claude-0/site/about.py from src_draft.html (shares the homepage CSS, nav, footer, Lenis, menu, glass nav, floaters, reveal and leader-card JS); writes about_src.html + about.html (full document, images inlined). Publish: copy about.html to the scratchpad and pass files={"about.html": ...}. Backups: about_v1.py–about_v3.py.
Sections now:
- Hero (v16, user: "no starting scroll effect, static is enough; title line by line is nice; drop 'Powered by progress'; smaller font"): static full-screen photo (sample proj3), breadcrumb, two lines "Built on a legacy." / "Driven by a vision." rising on load, font clamp(38px,5vw,76px), "Since 1996 · Palakkad · Kochi", scroll cue.
- Our story: photo opens via clip-path, quote fills word by word, one paragraph, then 1996 / 2013 / 4–5 MW / 2 offices under a yellow rule.
- Milestones 1996–2026: centre line fills yellow as you scroll; years about 30% smaller (v17: clamp(40px,4.6vw,72px), phones 38px).
- Vision & Mission (dark), word-by-word fill, three principles (Build with purpose / Deliver with responsibility / Keep progressing).
- Manufacturing & recognition: 5 site cards (Kanjikode 1996, Thodupuzha 2002, Coimbatore 2008, Qatar, Kanjikode Industrial Area 2024 = Sinelab) + 2018 Asianet Keerthimudra award card (photo placeholder).
- Leadership (v17, user: "add the rest of the team from the content doc"): 4 people with bios from the content doc – Sajeev Kumar K (MD, co-founder), Sunil Joseph (Director, co-founder), Athul S. Krishna (CMO), Sravan Paul Sunil (COO). Desktop: four tall cards that widen on hover/focus; tablet: 2×2 with bios shown; phone: swipe row.
- Closing CTA (v17, user disliked the yellow band): white section with a dark rounded card, night photo fading in on the right, "Let's power your next move", Get a free quote + Call +91 99462 07738, email / offices / since 1996.
axe: 0 violations desktop + phone. Comment threads for v16–v17 answered and resolved.
Homepage links changed to about.html (nav, menu, Discover our story, footer). Other nav items still point to homepage sections until those pages exist.
To verify with client: award name/year, SARK Cables spelling, Thodupuzha details, Qatar entity.

About page approved by the user (23 Oct, "yeah good").

## Solutions page (23 Oct, draft v18 – awaiting review)
User chose: Solutions next, one page (no per-service detail pages). Built by /tmp/claude-0/site/solutions.py (backup solutions_v1.py) from src_draft.html + about.py's CSS; drawings from /tmp/claude-0/site/iso.py. Published as solutions.html inside the draft artifact (files={"about.html": ..., "solutions.html": ...}, copies in the scratchpad /site folder).
- Hero: same template as About (static photo, sample pj_array; two lines rise on load): "One partner for / every energy need." · Homes · Businesses · Industries.
- Services: "Eight ways we power progress" + jump chips 01–08. Desktop: a sticky dark plate on the left shows an isometric line drawing (maquette on a plinth) for the service nearest the middle of the screen; it builds piece by piece, yellow dashed power flows move, the O&M one has an inspection sweep; counter 01/08 with progress bar. Right: one block per service – number, tag, title, the content-doc description, three "included" points restated from the doc's own wording, "Ask about …" link to the contact form. Phones: the drawing sits above each service.
- On-grid / off-grid / hybrid comparison table (grid, battery, power cut, extra power, best for; wording matches the homepage section) with a link to the homepage 3D section. Phones: rows turn into cards.
- How we work (dark): Assess, Design, Guide, Install, Support – the line fills as you scroll (vertical on phones). Wording from the FAQs / O&M copy.
- FAQs (6 of the approved 8, light version), closing dark card ("Find the right fit for your site"), footer.
- Homepage changes (systems2.py steps 8–9): nav/menu/footer Solutions links → solutions.html (footer items → #residential, #commercial, #storage, #lighting); each homepage solution card now opens its section on the Solutions page; "Explore all solutions" link under the cards; FAQ questions get the two-tone focus ring; in-page smooth-scroll links re-sync with the real scroll position first.
- About page: breadcrumb and email links padded to 24px targets.
- Checks: axe 0 violations on homepage, About and Solutions (desktop + phone); keyboard pass (focus ring on every stop, nothing under the nav, jump links move focus to the service); reduced motion shows everything static.
- To verify with client: "Made at our Kanjikode facility" (lithium batteries/inverters), "From a single building to megawatt scale", photos for each service (drawings can stay or be swapped for real photos).

## Later changes (23 Oct, draft v19–v22)
- Solutions page: jump links became dark illustrated tiles (4 on top, 4 below; 2 per row on phones). Drawings build in a wave on arrival; hover lifts, zooms, animates the power flow, yellow underline + arrow.
- About page: the 2018 award card moved into its own "Recognition" section between Our story and Milestones (#recognition); the manufacturing section is now labelled "Manufacturing".
- Tagline everywhere is "Powering Your Tomorrow" (footer on all pages + homepage hero h1; systems2.py step 10). The hero change goes beyond the comment: revert if the user/client wants "Powering Tomorrow" in the hero.
- Homepage solutions (user: "make something creative"): the 8 grey cards are now a numbered index list on the left + a sticky dark illustration plate on the right (same isometric drawings); hover/focus a row → it slides, gets a yellow underline, the tag turns yellow, an arrow appears and the plate builds that drawing. Rows link to solutions.html#id. Phones: swipeable cards with their own drawings (Lenis ignores .si-list on ≤900px). systems2.py step 11 (imports iso.py).
- Calculator bug (user: "why the amount is cut"): the bill amount box was sized once on load, before Inter Tight loaded / before the frame resized, so "₹4,500" could be clipped. Now re-measured after fonts load, on resize and via a ResizeObserver (systems2.py step 12).

## Projects page (23 Oct, draft v24 – awaiting review)
User: grid + case-study pop-up was the default (they didn't pick; asked "is there 7 case studies?" – yes, content doc section 5 lists 7; homepage shows 6 because SA Square's capacity is pending). Visuals: sample photos (user's choice).
Built by /tmp/claude-0/site/projects.py → projects.html (published as a file of the draft artifact, with about.html and solutions.html).
- Hero (same template, sample day.jpg): "Projects that / power progress." · Rooftop · Ground-mounted · Industrial · Residential.
- "From 20 kW homes to 1 MW plants": filter buttons with counts (All 7, Rooftop 4, Ground-mounted 1, Commercial & industrial 3, Residential 2; aria-pressed + live "Showing n projects"); grid of 3 – Pyarelal wide on row 1, Saleem Residence wide (image right) on row 3, so 7 cards fill 3 rows; cards rise in, photo zooms on hover.
- Case-study dialog (native <dialog>, focus trapped, Esc / backdrop / × close, focus returns to the card): photo, type, status, name, capacity / location / type, summary from the content doc, "Project note" only where the doc gives one (theatre: steep roof → raised installation; Bala: shading → Enphase microinverters; SA Square: access and structure), "Discuss a similar project", prev/next arrows (also ← →) through the visible projects. Phones: full-screen sheet.
- "Every size, one standard": capacity bars (1 MW … 20 kW) grow on scroll; SA Square left out until its capacity is confirmed.
- Closing dark card ("Let's build your next one"), footer.
- Homepage (systems2.py step 13): nav, menu and footer Projects links → projects.html; "View all projects" link under the homepage project slider.
- Checks: axe 0 on all pages (dialog open too); keyboard through the dialog.
- projects.html is ~3.1 MB because the sample photos are inlined; the Netlify build will use separate image files.

## Projects grid + nav (23 Oct, v25–v26)
- Projects grid (user: "feels congested"): now a staggered two-column layout – large photo (5:4), caption below (number, type, status; name + capacity; thin rule that turns yellow on hover), right column sits lower; hover shows a yellow "View project" pill on the photo. Phones: one column. Stagger is layout (kept with reduced motion).
- Navbar (user): "Our People" removed from the nav and phone menu on all pages (menu now 01–05). Team section stays on the homepage/About, footer link kept (offered to remove). systems2.py step 14.

## Gallery page (23 Oct, draft v27 – awaiting review)
Built by /tmp/claude-0/site/gallery.py → gallery.html (lighter photo copies layers/g_*.jpg). Content doc section 9: "A glimpse into our world", 4 categories; agency note says no stock imagery may be presented as Sinelab work.
- Top (v28, user: "one image, then flipping card to the next, for the major highlights; then all photos below"): dark highlights section replaces the photo hero. Left: "A glimpse into our world." + caption (01/05, type · capacity, name, one line), prev/next arrows with 5 progress bars, "Skip to all photos". Right: a deck of 5 sample photos (Pyarelal, Mannukkad, Sree Devi Durga Theatre, Bala Cinemas, Saleem Residence); the top card flips over (3D) and its back shows the next photo, the cards behind move forward. Desktop: tall section with a sticky inner, scroll turns the cards (~72vh per flip); arrows scroll to each card. Phones: arrows or swipe. Reduced motion: no tall section, photos cross-fade. One render(p) function draws every state; deck images reuse the grid's embedded photos (data-g), so each photo is embedded once. Previous version: gallery_v1.py.
- (v29, user: "not like flip, just going sideways and showing the next image") The highlights now slide sideways: current photo slides left and fades (clipped at the stage's left edge so it never covers the text), the next one slides in from the right where it peeks. The flip version is in gallery_v2.py.
- (v29, user on the black "Photo to be added" tiles: "I'll give you photos, or just use the photos we already have") Placeholder tiles removed: the grid shows only the 10 sample photos ("Our work in pictures"). Category cards and filters appear automatically once a second category has photos (code kept). Shot list still wanted from the client: lithium battery assembly (Kanjikode), integrated inverter testing, industrial lighting production, Kanjikode facility; installation crew on a rooftop, commissioning a plant, engineers at work; 2018 Asianet Keerthimudra Award, flagship 1 MW rooftop 2026, 20 kW off-grid Nelliampathy 2019.
- (v27) Hero was the standard photo template: "A glimpse into / our world."
- Four category cards (dark fill slides up on hover / when selected) + filter buttons with counts (All 20, Installations 10, Manufacturing 4, People 3, Milestones 3); gallery.html#manufacturing etc. opens with that category selected.
- Masonry (3 / 2 / 2 columns) of 20 tiles: 10 labelled sample photos (installations) and 10 dark "Photo to be added" tiles that double as a shot list (battery assembly, inverter testing, lighting production, Kanjikode facility; installation crew, commissioning, engineers; 2018 award, 1 MW rooftop 2026, Nelliampathy off-grid 2019). Tiles wipe open as they scroll in.
- Full-screen viewer (native <dialog>): photo or placeholder, category + caption, prev/next, ← →, swipe, Esc; focus returns to the tile.
- Note under the grid says sample photos are placeholders, not Sinelab projects.
- Homepage (step 15): nav/menu/footer Gallery → gallery.html; the 4 "View photos" buttons → gallery.html#category; "View full gallery" → gallery.html.
- Checks: axe 0 (viewer open too).

## Contact page (23 Oct, draft v31 – awaiting review)
User chose: enquiry form, quick contact options, offices with map spots (no FAQs). Built by /tmp/claude-0/site/contact.py → contact.html.
- Dark top: "Let's power / your next move." + content-doc intro; three quick-contact tiles (Call, WhatsApp wa.me/919946207738, Email) that fill yellow on hover.
- Enquiry: left "Tell us about your project" + 3 steps (we call you back / we look at your bills and site / recommendation and quote), sticky on desktop. Form per content-doc spec: full name*, phone* (Indian mobile check, hint), email (optional, format check), "I'm interested in" as 4 radio tiles (Residential, C&I, Hybrid & battery, Other), project requirements, consent line. Inline errors per field (aria-invalid + aria-describedby) + summary (role=alert), focus to the first problem; success panel (role=status, focus moves to it) with a "preview only" note; honeypot field; data-netlify="true" + form-name ready for Netlify Forms (the preview JS stops real submission – switch to a real submit at deploy).
- Offices: Palakkad and Kochi cards with stylised map spots ("Map to be added", pulsing pin), "Full address to be confirmed", phone and email. Registered name shown.
- (v33, user sent the two Google Maps links) Offices section is now one large Google Map (keyless embed, z=16) with a floating "Our locations" panel: 01 Palakkad office – Sinelab Technologies Pvt Ltd, Prathiba Nagar, Chandranagar Colony, Palakkad, Kerala 678007 (place_id ChIJDznElBNtqDsRwlGeDS40paQ); 02 Kochi office – Sinelab Solar, Mahakavi Vailoppilli Rd, Ponnurunni, Vyttila, Kochi, Kerala 682032 (place_id ChIJcaY_7vENCDsRLxtGqYodVqE). Choosing an office pins it on the map; each has Get directions (Google Maps directions, new tab) and Open in Google Maps. Hours "Mon–Sat 9:00 am–5:30 pm" come from the Google listings – confirm with the client. Phones: map on top, offices below. The review artifact may block the embed; it works on the live site. Patch script: contact_maps_patch.py; previous: contact_v2.py.
- Site-wide (systems2.py step 16): nav Contact, nav/menu "Get a free quote" → contact.html; footer "Palakkad · Kochi" → contact.html#offices; About/Solutions/Projects/Gallery buttons that went to index.html#contact now go to contact.html. Homepage body CTAs still scroll to the homepage contact section.
- Checks: axe 0 on all six pages; form keyboard + error flow tested.
All main pages are now drafted. Still to do before Netlify: client approval, legal pages (Privacy Policy, Terms – content doc has drafting briefs, needs legal review), real photos/addresses/map links, deploy.py multi-page build (separate image files), switch the form to real submission, remove robots noindex at launch.

## Mobile + map fixes (26 Oct, draft v34–v35)
- About team (user: "make the cards vertical for mobile"): phones (≤700px) stack the 4 leaders as vertical cards – photo, then name, role, bio. Lenis prevent no longer applies to .ab-leaders. Homepage team still a swipe row on phones (offer to match).
- Solutions comparison (user: "make it easy for mobile, visually"): phones show 3 system cards (On-grid / Off-grid / Hybrid) with icon, "Best for…", three Yes/No tiles (Grid, Battery, Power-cut backup; yes tiles yellow) and "Extra solar power"; the table is hidden on phones. Patch: sol_cmp_patch.py.
- Projects filters (user: "make it mobile friendly"): phones show all filters at once – All full width, then two per row, rounded tiles with counts.
- Contact map (user: "where's the map, optimise this section"): the review artifact blocks Google, so only the drawn map showed. Section is now a compact two-column block (offices list left, map right, ~460px tall; phones: map first). Behind the Google Map sits a location card (pin, name, address, Open in Google Maps) that shows when the map can't load (CSP violation event, file: or offline). Offered: use client screenshots of Google Maps as a static picture. Patch: contact_map2_patch.py; previous contact_v3.py.

- Contact map v36 (user: "pin 2 locations directly in map, don't make users choose"): replaced the Google embed with one drawn map of central Kerala – coastline from Natural Earth 10m (public domain, via npm world-atlas, clipped to lon 75.55–77.35, lat 9.75–10.95; /tmp/claude-0/geo/mkmap.py → land.json), NH 544 line through approximate town points, Thrissur/Aluva/Walayar dots, "Arabian Sea", and both office pins (links to the Google Maps place) with labels. Map keeps the drawing's aspect (1000/678) so pins line up; phones crop to the strip between the offices (aspect 600/678). Both office cards are always open; card and pin highlight together (class is-hl; ".hl" clashes with a homepage class). Works in the preview. Patch: contact_map3_patch.py; previous: contact_v4.py.

## Netlify package (26 Oct)
User asked for Netlify steps (all pages done). Netlify project: "sinelabtest" → sinelabtest.netlify.app (Netlify Drop, last deploy Oct 22 = old v48 homepage).
Built by /tmp/claude-0/site/deploy2.py from the CURRENT draft sources (src_draft.html + about/solutions/projects/gallery/contact *_src.html) → /tmp/claude-0/deploy/sinelab-website (84 files, 12.6 MB) → /mnt/user-data/outputs/sinelab-website-netlify.zip (11 MB, index.html at the zip root).
- Real image files, self-hosted GSAP/ScrollTrigger/Three/Lenis and Inter Tight; per-page <title>/description; robots noindex kept (review build); _headers (cache + nosniff + referrer policy); favicon.
- Forms live via Netlify Forms: homepage form "homepage-enquiry", Contact form "enquiry" (data-netlify, form-name, honeypot); JS posts with fetch and shows a clear error ("call or WhatsApp") if sending fails. Preview-only notes removed.
- Checked over a local server: no 404s, no external requests, no console errors, axe 0 (homepage headings can read low mid-animation only).
- Steps given: Forms → Enable form detection; drop the zip on the project; test a submission; Form notifications → email info@sinelabtechnologies.com; rollback via Deploys → Publish deploy.
- Before the real-domain launch: remove noindex on all pages, Privacy Policy + Terms pages, real photos/hours confirmation, domain + MX records.
- DONE (26 Oct, user): zip deployed to sinelabtest.netlify.app, form detection enabled, redeployed, email notification set up (info@sinelabtechnologies.com). Future updates: send a new zip from deploy2.py; user drops it on Project overview. Rollback: Deploys → older deploy → Publish deploy.

## WCAG skill (23 Oct)
User added a "wcag-accessibility-expert" skill (saved from their uploaded file, with two fixes: 2.4.11 = Focus Not Obscured, 2.4.13 = Focus Appearance; focus trapping only for modal dialogs). Use it together with the A11y Enforcer plugin for every page.

## Client review PDF (23 Oct)
/mnt/user-data/outputs/Sinelab_Homepage_Review.pdf – 8 pages: cover + two desktop sections per page (user asked for less detail; a 34-page desktop+phone version was replaced). Built by /tmp/claude-0/pdfbuild/build_short.py from /tmp/claude-0/site/capture_pdf.js screenshots (DONLY=1 for desktop only).
Site change after approval: the "Reasons to choose us" heading is now "About <em>us</em>" (systems2.py step 6; src.html/src_v50.html; draft artifact v13). The intro section's small label also says "About us" – flag if the client minds. Re-run deploy.py before the Netlify hand-over.

## Release status (23 Oct, later)
User approved draft v12 ("final approval"), then said: WAIT FOR CLIENT APPROVAL before it goes to Netlify.
- Local source promoted: src.html = approved draft (backups src_v48_backup.html, src_v49.html). Main preview artifact NOT republished (user declined that publish) – it still shows v48; the draft artifact shows the approved version.
- Netlify package built and verified: /tmp/claude-0/deploy/sinelab-website (index.html 213 KB, 9.8 MB total, _headers for Netlify cache, vercel.json kept). Not sent yet; homepage only. When all pages are done and the client approves: extend deploy.py for multi-page, rebuild, zip, send; Netlify > site > Deploys > drag the folder in; rollback = Deploys > older deploy > Publish deploy.

## Hosting status (23 Oct)
- Vercel (sinelab-website.vercel.app, repo poojaguneshuiux/sinelab-website): still serves the OLD index.html; the v48 upload landed as index_1.html and the user couldn't find delete/rename in GitHub. Direct fix links: github.com/poojaguneshuiux/sinelab-website/delete/main/index.html, then /edit/main/index_1.html (rename).
- User then said they "connected to Netlify"; method and URL unknown. Netlify ignores vercel.json. Netlify Forms could connect the contact form.
- No GitHub/Vercel/Netlify access from Claude; never ask for or use the user's credentials.
- index.html has robots noindex (sample content): REMOVE AT LAUNCH. Contact form not connected yet.
- Vercel Hobby is non-commercial; keep MX records when changing DNS for sinelabtechnologies.com.

## Real project photos (29 Oct, draft v38 – awaiting review)
User sent four drone photos (in their Downloads: "BAVA Metals 35Kwp .PNG", "Grand Bajaj Showroom 70KWp.JPG.jpeg", "Bala Cinemas 70KWp.JPG.jpeg", "Jamal Sons 30 KWp.JPG.jpeg") and chose: only these four projects, shown WITHOUT capacity for now.
- Images: /tmp/claude-0/realimg (EXIF-rotated) → site/layers real_{bava,bajaj,bala,jamal}{_card 5:4, _slide 16:10, tall}.jpg + real_bala_hero.jpg.
- Projects page (projects_real_patch.py; backup projects_v3.py): 4 cards (sector label + arrow, no capacity, no filters), hero = Bala Cinemas photo, h2 "Rooftops we have put to work", capacity chart removed, dialog spec = Type + Sector. The seven content-doc projects (Pyarelal, Mannukkad, Sree Devi Durga, Boopathi Steels, Saleem, SA Square) are no longer shown.
- Homepage (step17_real.py, run once; backup src_v51_pre_real.html): featured slider = the 4 real projects (/ 04, names link to projects.html#id); Gallery panel 01 uses the Bala photo.
- Gallery (gallery_real_patch.py + gallery_real2_patch.py; backup gallery_v3.py): highlights deck = the 4 real projects; "Sinelab projects" row (4 real photos, full photos in the viewer) above a "Sample photos" masonry (still labelled).
- Netlify zip rebuilt (deploy2.py, 89 files, 14.9 MB): user re-drops it on sinelabtest.netlify.app.
- Later (29 Oct, draft v40): two more real projects from DNG drone files (developed with rawpy, corners lifted, 90% centre crop): Palakkad Surgicals (file: 30 kWp, sector Manufacturing) and Sinicon (file: 70 kWp, Industrial), added as projects 05–06 on Projects, homepage slider (/ 06) and Gallery (real row now 3 columns, 4:3). real6_patch.py; backups src_v52_pre_real6.html, gallery_v4.py, projects_v4.py.
- About team (29 Oct): Saran and Leenu Joseph added ("Designation to be confirmed", tag "Team"; user will send designations). User said the 6-in-a-row layout was "not nice", so it's now: two co-founders as large side-by-side cards, then four equal cards (about_team_patch.py; backups about_v6.py, about_v7.py). Homepage team still shows the original four.
- Project films (homepage "Projects in motion", draft v41): user asked for Palakkad Surgicals and Sinicon there "as milestones". Now 2 slides ("Milestone projects, from above"); no drone video yet, so each clip is a 10 s slow push-in rendered from the real photo (/tmp/claude-0/films2/mk.py → site/media/psurg|sinicon .mp4/.webm). Sample clips moved to site/media_old. step19_films.py; backup src_v53_pre_films.html. Swap in real drone videos when the user sends them.
- Later (draft v42): user sent a 2000×1125 photo of "their 1 MW rooftop" for milestone slide 1. Labelled Pyarelal (the content doc's only 1 MW rooftop) – ASSUMPTION, confirm with user. Clip media/mw1.mp4/.webm; films now 3 slides (Pyarelal, Palakkad Surgicals, Sinicon). Backup src_v54_pre_mw.html. Not yet on the Projects page or Gallery (offered).
- Sharper films (draft v43, user: "upscale the milestone images a bit"): /tmp/claude-0/films2/mk2.py renders 1920×1080 with Lanczos + light unsharp; MP4 re-encoded CRF 22 capped 3.2 Mbps (~4 MB each), WebM CRF 33; posters 2000×1125. EDSR AI upscale tried (opencv 4.10 venv /tmp/claude-0/srenv) but too slow on 2 CPUs (~25 min/photo) and little gain since the 1 MW source is already 2000 px wide. Netlify zip now ~32 MB.
- TO CONFIRM: capacities from the file names (Bava 35 kWp, Grand Bajaj 70 kWp, Bala 70 kWp, Jamal 30 kWp). Bala Cinemas conflicts with the content doc (170 kW). Locations/status of the other three unknown.

## Team photos (29 Oct, draft v44)
User: "now lets add fotos of the team". Only "Athul Pro.jpeg" (1184×864) was in Downloads: cropped to layers/team_athul_sq.jpg (About card) + team_athul_tall.jpg (homepage card). about.py PHOTOS dict maps name → (square, tall); add more there. Waiting for photos of Sajeev, Sunil, Sravan, Saran, Leenu. Also noticed in Downloads (not used yet): 4 DJI drone photos (DJI_2025…_D.JPG.jpeg, ~26 MB each, 29 Oct 09:28) and "kanjikode solar 3.mp4" (24 MB).

## Team photos, all (29 Oct, draft v45)
User sent 5 photos + Saran.pdf / Leenu_jose.pdf (each PDF = one photo, no designation) and said: add Ravinder Mehta to About; homepage = Sajeev, Sunil, Athul photos; About = everyone. Crops by face detection (/tmp/claude-0/team/crop.py, OpenCV 4.10 venv) → layers/team_{key}_sq.jpg (800²) and _tall.jpg (720×960).
- Photo matching ASSUMED (confirm): Sunil = BNI badge photo (certain), Athul = "Athul Pro" (certain), Saran/Leenu = their PDFs (certain); Sajeev = older man with glasses (navy blazer, lanyard), Sravan = young man in grey blazer on white, Ravinder Mehta = grey beard, denim shirt, blue backdrop.
- About team: 2 founders + row of 5 (Athul, Sravan, Saran, Leenu, Ravinder); 3 per row ≤1100px, list ≤820px. Saran, Leenu, Ravinder: "Designation to be confirmed", tag "Team". User (comment): team row shows name + designation only (bios removed for Athul and Sravan); the two founders keep their bios. Backup about_v10.py. Backups about_v8/v9.py, src_v55/v56.

## Salim Hybrid Residence (29 Oct, draft v47)
User sent a top-down drone photo (1920×1080); first said "add to 1MW project card", then corrected: it's not 1 MW, add it as a project named "Salim Hybrid Residence" (= content doc's Saleem Residence, 20 kW hybrid). Added as project 07 (Residential, Hybrid solar, content-doc summary, no capacity) on Projects, homepage slider (/ 07) and Gallery (real row now 4 columns). salim_patch.py; backups projects_v5.py, gallery_v5.py, src_v57_pre_salim.html. The 1 MW milestone slide (Pyarelal, factory roofs photo) is unchanged.
- Then user: "add salim hybrid residence to highlight section too, just replace any one from highlight" → read as the Gallery top deck (user earlier called it the "major highlight"): Salim replaces Jamal Sons there (6 slides). Jamal Sons is still on Projects, homepage slider and the gallery grid. If they meant the homepage milestones instead, swap there.

## 29 Oct, draft v48
- Milestone films now 3 s each (user comment), then auto-advance; gentler zoom (1.10–1.14). /tmp/claude-0/films2/v3 (mk3.py = mk2.py with a duration arg). Clips ~1.3 MB each.
- Homepage projects slider: Salim Hybrid Residence moved to 3rd (Bava, Grand Bajaj, Salim, Bala, Jamal, Palakkad Surgicals, Sinicon). Projects page order unchanged. Backup src_v58_pre_order.html.

## Pages open at the top (29 Oct, draft v49)
User: switching pages after scrolling to the bottom opened the next page at the bottom. Fix in the shared core script (src_draft.html, lifted into every page): history.scrollRestoration = 'manual' + ScrollTrigger.clearScrollMemory('manual') (ScrollTrigger otherwise flips it back to 'auto'), scroll to 0 at start, Lenis scrollTo(0) after init, again on load (unless the visitor already scrolled) and on bfcache pageshow. Links with a #section still land on the section. Tested on the deploy build: footer links from page bottom → new page at 0; about.html#ab-team and contact.html#offices still land on their sections. Backup src_v59_pre_top.html.

## About › Recognition redesign (29 Oct, draft v50)
User comment: "add some background elements here, it feels so gap". rec_patch.py (backup about_v11.py): section pulled up into the gap with a dotted backdrop + warm glow and 7 slow-drifting line icons (sun, ring, medal, leaf, sparks); award card now dark with a drawn emblem (rotating dashed rays, laurel wreath, trophy, twinkling sparks; SVG also saved as site/rec_emblem.svg) and a large outlined "2018" behind the text; year as a yellow pill. "Award photo to be added" note kept. Reduced motion stops the animations.

## Designations (29 Oct, draft v51)
Saran = Regional Manager, Kochi Division; Leenu Joseph = Project Engineer, Kochi Division (division shown on a second line). Ravinder Mehta = Head of Solar Division (tag changed to Leadership and moved after Sravan; backup about_v13.py). Backup about_v12.py.
User asked to "connect to Vercel directly": no Vercel connector in the registry; I won't sign in with credentials. Explained the options (stay on Netlify, recommended, forms work; or Vercel via GitHub upload, but Netlify Forms would stop working there without a form service such as Formspree). User said "ok wait", so this is open.

## Vercel (29 Oct)
User: "lets connect this to vercel https://vercel.com/pooja-5b72". No Vercel connector; the browser pane showed the Vercel login (I don't sign in for the user; they started signing in with Google in the pane themselves). Built a Vercel version: /tmp/claude-0/site/deploy_vercel.py → /tmp/claude-0/deploy/sinelab-website-vercel (from the Netlify build): forms post to FormSubmit AJAX (info@sinelabtechnologies.com, one-time activation email), _honey/_subject/_template/_captcha fields, vercel.json headers, no _headers. Tested with a mocked FormSubmit response (success and failure paths). Zip: /mnt/user-data/outputs/sinelab-website-vercel.zip, also saved to the user's Downloads. Deploy path: upload to the GitHub repo connected to Vercel (two uploads: root files + media, then assets; GitHub web limit is 100 files per upload). Rollback: Vercel › Deployments › previous › Promote to Production / Instant Rollback. Vercel Hobby plan is for non-commercial use.

## WebP + performance (29 Oct, draft v53)
User: "convert all images to webp and optimise the website performance as the website is lagging".
- webp_cache.py: every image goes through a WebP cache (/tmp/claude-0/site/webp): photos q72, longest side 1920 (cards/portraits/thumbs 1200, video posters 1280); logos keep transparency. All preview builders (build_draft.py + 5 page builders) inline WebP; deploy2.py ships assets/img/*.webp and adds decoding="async" to every <img>. Only apple-touch-icon.png and og.jpg (new 1200×630 social-share image from the Bala Cinemas drone photo) stay non-WebP. Backups *_prewebp.py.bak.
- Used images 13.4 MB → 8 MB; preview pages shrank (gallery 8 → 4.8 MB, projects 4 → 2.1 MB, home 6.3 → 5.3 MB); homepage first load ~2.7 MB.
- Runtime (src_draft.html, shared by all pages; backup src_v60_pre_perf.html): 3D model pixel ratio capped (1.5 desktop / 1.25 phones, was 2), PCFShadowMap + 1024 shadow map (was soft 2048), phones use native touch scrolling (Lenis syncTouch off), sample-photo labels no longer use backdrop blur.
- Checked: no console errors, no broken images on any page (desktop + phone), axe 0 issues. New Vercel folder saved as Downloads\sinelab-website-vercel-v2 (old sinelab-website-vercel folder is outdated).

## Hero image clean-up (2 Nov, draft v54)
User: hero trees looked doubled/blurred at the sides (old wide image = original 1536x1024 photo + mirrored, blurred side bands). Rebuilt the 2410x1196 scene without mirroring or blur: /tmp/claude-0/hero2/compose.py + build3.py -> hero2/wide_clean.png (clean sky gradient measured from the photo; both trees now end with real leafy edges borrowed from the big tree's own edge, colour-matched on the left; hedges, planting bed, lawn and shrubs continue from real texture). Layers rebuilt by hero2/build_layers2.py (copy of hero/build_layers.py: band sky reaches down to the hedges, sky gaps inside crowns count as sky, edge pixels take the nearest foliage colour so there is no pale outline at dusk/night). Window/lamp positions unchanged. Old layers backed up in site/layers_backup_prehero. LaMa (OpenCV zoo ONNX) was tried for outpainting but gave dark smears.
Changed deploy files: assets/img day, fg_day, fg_dusk, fg_night, stars, panels, win0-8 (.webp) - also copied into Downloads\sinelab-website-vercel-v2.

## Pending from client
Drone videos; vector logo; award photo; more real project photos + capacities for the four real projects (Bala 70 vs 170 kW); leadership portraits (4 now: Sajeev, Sunil, Athul, Sravan); gallery photos; addresses + map links; social URLs; approved testimonials; legal review.

## Claude Code handover (2 Nov)
User: "i want to transfer this to claude code so give me neccessary handover files". Built /tmp/claude-0/handover/sinelab-website (199 files, 36 MB):
- site/ = current Vercel build (source of truth from now on; Vercel Root Directory = site); assets-source/ (brand pack, real project + team photos, hero sources); docs/HANDOVER.md (state, content facts, assumptions, open items), docs/history-notes.md (this log), docs/reference (client PDFs + WCAG skill), docs/legacy-build (old generators, reference only); tools/check.js (axe WCAG 2.2 AA + console/404/broken-image/external-request check, desktop + phone), tools/screenshots.js, tools/to_webp.py, tools/make_film.py; package.json (serve/check/screenshots), CLAUDE.md (rules + code map), README.md, .claude/skills/wcag-accessibility-expert.
- All four tools tested; check = "All pages clean".
- Delivered: /mnt/user-data/outputs/sinelab-website-claude-code.zip (34.5 MB) and the unzipped folder Downloads\sinelab-website-claude-code on the user's PC (.claude folder can't be written remotely; CLAUDE.md says to copy docs/reference/WCAG_Accessibility_Expert_Skill.md into .claude/skills if missing).
- Found while documenting (listed in HANDOVER open items): homepage about.webp + blog1–3 are sample photos without a "Sample photo" label; footer social + Privacy/Terms links point to index.html.

## Live-site check (3 Nov)
User asked for "the updated link". Checked in the browser pane:
- sinelab-website.vercel.app: still the OLD homepage-only build (day.jpg, no subpages – about/solutions/… 404). The latest Vercel build was never uploaded to GitHub.
- sinelabtest.netlify.app: all 6 pages, real projects, films, designations (29 Oct build) but BEFORE the WebP/performance pass and the 2 Nov hero clean-up (day.webp 404).
- Latest version is only in the draft artifact (https://claude.ai/artifact/9RiaKn4eWfiFizxFp1vVCU, v54).
- Made /mnt/user-data/outputs/sinelab-website-netlify-latest.zip (111 files, 16.7 MB, = /tmp/claude-0/deploy/sinelab-website minus README.txt; identical to the handover site/ except Netlify Forms instead of FormSubmit; check.js all clean). Also saved to Downloads\sinelab-website-netlify-latest.zip. User drops it on the Netlify project → sinelabtest.netlify.app updates; rollback = Deploys → previous deploy → Publish deploy.
- User (3 Nov): "you don't have to connect Vercel, just the preview is enough". Vercel is dropped for now; the review link is the draft artifact https://claude.ai/artifact/9RiaKn4eWfiFizxFp1vVCU (last updated 2 Nov = latest). Keep publishing updates there.

## Homepage projects grid (3 Nov, draft v55)
User comment on #projTrack: "change the layout, avoid the scroll to see projects, show it in one glance, just 3-4 then a CTA to view projects". projects_grid_patch.py (backup src_v61_pre_pgrid.html) replaced the pinned sideways slider with #projGrid:
- Desktop: Bava Metals large (left, spans 2 rows; real_bava_feat = full 1828x1056 source, object-position 42% 50%), then Grand Bajaj (object-position 50% 25%), Salim, Bala as 16:10 tiles (real_*_tile 1000x625), then a dark "View all 7 projects" card (round photos of Jamal, Palakkad Surgicals, Sinicon = real_*_dot 160px, "+3", yellow arrow) → projects.html. Whole cards clickable (stretched link), card focus ring via :has().
- Short laptop screens: small photos max-height max(130px, (100svh - 470px)/2), so 1280x720 and 1366x768 show the whole grid in one view.
- Tablet ≤1023: Bava across the top (16:8), three in a row, "View all" as a full-width bar. Phones ≤700: Bava (4:3), then a compact list (112px thumbs), then the tile.
- Wipe-in reveal with stagger + sunlight glint (IntersectionObserver); reduced motion shows everything static. Old slider CSS/JS/phone CSS and the Lenis prevent for .proj-track removed. real_*_slide images no longer used (still present in the user's PC handover folder; safe to delete).
- check.js: all pages clean. Published draft v55; deploy builds, handover site/, CLAUDE.md, HANDOVER.md updated; zips rebuilt.

## Design system (3 Nov)
User: "give me the brand design system of this website". Made from the Design System artifact type: https://claude.ai/artifact/FrUK97GBoiJxafei1TmxCE ("Sinelab Design System", private until shared). Local source: scratchpad/ds/project (README brand book, tokens.json, components/bundle.css + 10 components with previews and guidelines, cover, asset group READMEs, 5 Inter Tight latin woff2).
- Tokens: 22 colours (site :root names kept: ink, card, paper, line, muted, slate, sun, amber→sun, accent-ink, navy/navy-deep→ink, on-dark, on-dark-muted, line-dark, surface-dark + field-line, placeholder, danger set, whatsapp), 15 type styles (Display/Headings/Text, desktop max of each clamp), 14 spacing, 8 radii (6/10/12/14/16/18/24/999), 5 shadows incl. focus halos, easing, duration, breakpoints, z-index. One theme ("Site"); dark bands use the on-dark tokens. Every value checked against site CSS; contrast ratios in each usage note.
- Components (static previews, site class names): Button, TextLink, SectionHead, NavBar, WhatsAppButton, ProjectCard, ViewAllCard, FAQItem, FormField, PhotoLabel. Not included: solutions index + isometric drawings, hero day/night scene, 3D model, savings calculator, team cards, gallery viewer, footer, mobile menu panel (described in NavBar).
- Assets uploaded: 5 logos, 14 icons (Dark Gold SVGs), 9 project photos, brand guidelines PDF. Cover: Sine(300)lab(600) + rooftop panel grid with a diagonal of lit cells, sun disc, paper tile.
- Flagged: brand PDF still says tagline "Powering Tomorrow."; site uses "Powering Your Tomorrow".

## Font switch to Manrope (5 Nov, draft v56, AWAITING APPROVAL)
User asked why Inter Tight (is the logo Inter?). Honest answer: the logo font was never supplied; Inter Tight was my closest-match pick. Tested the wordmark against 11 fonts (canvas overlay, bbox-normalised IoU): Manrope 0.887 (Sine at 300, lab at 500, tight tracking) vs Inter Tight 0.74, others ≤0.62. The overlay is near-exact, so the logo is almost certainly set in Manrope. DM Sans (user's suggestion) scored 0.56 and has no tabular figures.
- Switched the whole site to Manrope (OFL; has tabular figures and ₹): Google Fonts link + --f-display/--f-body/--f-mono in src_draft.html, all *_src.html and the inlined preview pages; deploy2.py self-hosts /tmp/claude-0/fonts/manrope (latin + latin-ext 300–700). Backups in /tmp/claude-0/backup_pre_manrope/.
- Checked: no overflow or clipping on any page at 1440, 1024 or 390; nav pill 724px wide (fits from 901px); some headings and FAQ questions wrap one line more (e.g. film title "Powering Progress. At Scale." now 2 lines); check.js all clean.
- NOT yet synced (wait for approval): Claude Code handover folder and zip, Netlify/Vercel zips, design system (tokens type family, fonts/, README), brand guidelines PDF. Revert = artifact v55 or restore the backups.
