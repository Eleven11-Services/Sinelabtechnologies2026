# Legacy build scripts (reference only)

These Python scripts generated the site during the Cowork sessions (22 Oct – 2 Nov 2026). **Do not run them.** They read and write absolute paths in the old cloud workspace (`/tmp/claude-0/...`), and the source files they need (`src_draft.html`, the `*_src.html` page modules, `layers/`, the WebP cache) are not part of this handover.

`site/` is the source of truth now. Edit the HTML there directly.

They are kept here because they explain how some things were made:

| Folder | What's inside |
|---|---|
| `pages/` | Homepage source pipeline (`systems.py`, `systems2.py`, `build_draft.py`), the page builders (`about.py`, `solutions.py`, `projects.py`, `gallery.py`, `contact.py`), the isometric service drawings (`iso.py`), the patch scripts for later changes (`*_patch.py`, `step17_real.py`, `step19_films.py`, `real6_patch.py`, `salim_patch.py`), the WebP cache (`webp_cache.py`) and the deploy packagers (`deploy2.py` for Netlify, `deploy_vercel.py` for Vercel/FormSubmit) |
| `hero/` | Hero scene: `build_layers_v1.py` (original day/dusk/night layer cut-outs, window and lamp masks), `compose.py` + `build3.py` (clean 2410×1196 wide scene without mirroring), `build_layers2.py` (layers rebuilt from it with edge decontamination) |
| `media/` | `make_film_v3.py` (push-in clips, superseded by `tools/make_film.py`), `team_face_crop.py` (face-detection portrait crops, OpenCV 4.10 contrib), `contact_map_coastline.py` (Kerala coastline for the contact map, from Natural Earth via npm `world-atlas`) |

For new work, use `tools/` in the repo root instead.
