# Gallery follow-up: Sinelab's own photos get their own row above the sample masonry (in CSS columns they all fell into
# column one), and the viewer fits tall photos to the screen.
p = '/tmp/claude-0/site/gallery.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

rp("""        inner = f'<img src="{{{{L:{img}}}}}" data-g="{img}" alt="" loading="lazy">'""",
   """        inner = f'<img src="{{{{L:{img}}}}}" data-g="{img}" alt="" loading="lazy"' + (f' style="object-position:{FOCUS[img]}"' if img in FOCUS else '') + '>'""")
rp("REAL_IMGS = {it[1] for it in REAL}\n", "REAL_IMGS = {it[1] for it in REAL}\nFOCUS = {'real_bava.jpg': '30% 50%'}\n")
rp("tiles = '\\n'.join(tile(k, it) for k, it in enumerate(ITEMS))",
   "tiles = '\\n'.join(tile(k, it) for k, it in enumerate(ITEMS) if k >= len(REAL))\n"
   "real_tiles = '\\n'.join(tile(k, it) for k, it in enumerate(ITEMS) if k < len(REAL))")
rp("""    <ul class="gm" id="gm">
{tiles}
    </ul>
    <p class="gl-note">The first four photos are Sinelab projects. Photos marked “Sample photo” are placeholders, not Sinelab work, and will be replaced as more of Sinelab’s own photographs arrive.</p>""",
   """    <h3 class="gm-h">Sinelab projects</h3>
    <ul class="gm gm-real" id="gmReal">
{real_tiles}
    </ul>
    <h3 class="gm-h">Sample photos <span>Placeholders, not Sinelab work. They will be replaced as more of Sinelab’s own photographs arrive.</span></h3>
    <ul class="gm" id="gm">
{tiles}
    </ul>""")
rp(".gl-note{", ".gm-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin:0 0 clamp(18px,2vw,26px);padding-top:clamp(18px,2vw,26px);border-top:1px solid var(--line);font-size:clamp(20px,1.8vw,24px);font-weight:400;letter-spacing:-0.02em;color:var(--ink)}\n"
   ".gm-h span{font-size:14.5px;letter-spacing:0;color:var(--muted)}\n"
   ".gm-real{columns:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 clamp(14px,1.6vw,22px);margin-bottom:clamp(40px,5vw,72px)}\n"
   ".gm-real .gt{margin:0}\n.gm-real .gt .gt-img{aspect-ratio:4/5}\n"
   "@media (max-width:1100px){.gm-real{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:22px}}\n"
   ".gl-note{")
# viewer: give the stage a definite row so tall photos fit the screen
rp(".lb-stage{position:relative;display:grid;place-items:center;", ".lb-stage{position:relative;display:grid;grid-template:minmax(0,1fr)/minmax(0,1fr);place-items:center;")
rp("  const tiles = [...gm.querySelectorAll('.gt')],", "  const tiles = [...document.querySelectorAll('.gm .gt')],")
open(p, 'w').write(s); print('patched')
