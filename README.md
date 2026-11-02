# Sinelab Technologies website

A static website for Sinelab Technologies Pvt. Ltd. (solar, energy storage and lighting; Palakkad and Kochi, Kerala). There are six pages, plain HTML/CSS/JS, and no build step.

- **`site/`** is the website. Upload it, or point Vercel's Root Directory at it.
- **`CLAUDE.md`** has the working rules and how the code is organised. Claude Code reads it automatically.
- **`docs/HANDOVER.md`** has the history, content facts, assumptions and the open-items checklist.

## Open it in Claude Code

```
cd sinelab-website
claude
```

Ask for a change ("make the projects grid 3 columns on desktop", "add the award photo", and so on). Claude follows `CLAUDE.md`: it checks accessibility, shows you screenshots and asks before anything goes live.

## Preview and check

```
npm install
npx playwright install chromium
npm run serve          # open http://localhost:8000
npm run check          # errors, broken images, WCAG 2.2 AA (axe) on every page, desktop + phone
npm run screenshots    # PNGs of every page in ./screenshots
```

Python 3 is needed for `serve`. Pillow is needed for `tools/to_webp.py`, and Pillow plus ffmpeg for `tools/make_film.py`.

## Deploy (Vercel)

1. Push this folder to the GitHub repo connected to Vercel.
2. In Vercel, go to Settings → Build & Deployment and set Root Directory to `site`. Use framework "Other", with no build command.
3. Check the preview deployment, get approval, then promote to production.
4. To undo, go to Deployments → previous deployment → Instant Rollback.

At launch, remove the `noindex` meta tag from all six pages and complete the checklist in `docs/HANDOVER.md`.
