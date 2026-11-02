# Projects page: Sinelab's own drone photos of four real projects replace the seven sample-photo case studies (user, 29 Oct).
# Capacities are left off for now (user: "Show without capacity for now"), so the capacity chart and filters go too.
p = '/tmp/claude-0/site/projects.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

rp("# Projects page: all seven case studies from the content document.",
   "# Projects page: four real projects with Sinelab's own drone photos (29 Oct). Capacities to be added once confirmed.")
rp('Rooftop, ground-mounted, industrial and residential solar projects by Sinelab Technologies, from 20 kW homes to 1 MW plants in Kerala.',
   'Rooftop solar projects by Sinelab Technologies for Bava Metals, Grand Bajaj Showroom, Bala Cinemas and Jamal Sons.')
rp("\"['#work','#scale']\"", "\"['#work']\"")

# ---- data ----
a = s.index("# ---------- content (client's content document; photos are samples) ----------"); b = s.index("FILTERS = [")
s = s[:a] + '''# ---------- content: real projects, Sinelab's own drone photos ----------
# id, name, sector, card photo, focus (object-position), type, status, summary, note(title, text) or None, alt text
P = [
  ('bava-metals', 'Bava Metals', 'Commercial building', 'real_bava_card.jpg', '55% 50%', 'Rooftop solar', None,
   'Rooftop solar for Bava Metals, with the panels set along the building’s metal roofs on a busy town street.', None,
   'Drone view of the Bava Metals building, with solar panels along its metal roofs'),
  ('grand-bajaj', 'Grand Bajaj Showroom', 'Vehicle showroom', 'real_bajaj_card.jpg', '50% 45%', 'Rooftop solar', None,
   'Rooftop solar above the Grand Bajaj showroom. The panels stand on a raised steel frame over the flat terrace.', None,
   'Solar panels on a raised steel frame above the Grand Bajaj showroom, with the Bajaj and Chetak signs below'),
  ('bala-cinemas', 'Bala Cinemas', 'Cinema', 'real_bala_card.jpg', '50% 50%', 'Rooftop solar', 'Completed',
   'A completed rooftop installation incorporating Enphase microinverters to address site-specific shading conditions on a challenging roof.',
   ('Shading on a challenging roof', 'Enphase microinverters let each panel work on its own, so shade on one part of the roof doesn’t pull down the rest.'),
   'Drone view of the Bala Cinemas building with a solar array on its roof'),
  ('jamal-sons', 'Jamal Sons', 'Commercial building', 'real_jamal_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar for the Jamal Sons building, on a main road lined with shops.', None,
   'Drone view of the Jamal Sons building on a main road, with solar panels on its roof'),
]
''' + s[b:]
a = s.index("FILTERS = ["); b = s.index("def card(k, p):")
s = s[:a] + s[b:]

a = s.index("def card(k, p):"); b = s.index("CLOSE = '<svg")
s = s[:a] + '''def card(k, p):
    pid, name, sector, img, focus, typ, status, summ, note, alt = p
    st = f'<span class="pc-st">{status}</span>' if status else ''
    return f\'\'\'        <li class="pcard{" shift" if k % 2 else ""}" id="{pid}" style="--k:{k}">
          <button type="button" class="pc-open" data-k="{k}" aria-haspopup="dialog" aria-label="{name}, {sector.lower()}, {typ.lower()}{", " + status.lower() if status else ""}. View project">
            <span class="pc-img"><img src="{{{{{{{{L:{img}}}}}}}}}" alt="" loading="lazy" style="object-position:{focus}"><span class="pc-view" aria-hidden="true">View project {ARR}</span></span>
            <span class="pc-body">
              <span class="pc-top"><span class="pc-n">{k + 1:02d}</span><span class="pc-type">{sector}</span>{st}</span>
              <span class="pc-row"><span class="pc-name">{name}</span><span class="pc-go" aria-hidden="true">{ARR}</span></span>
            </span>
          </button>
        </li>\'\'\'
cards = '\\n'.join(card(k, p) for k, p in enumerate(P))

DATA = json.dumps([{'id': p[0], 'name': p[1], 'sector': p[2], 'focus': p[4], 'type': p[5], 'status': p[6], 'summary': p[7],
                    'note': p[8], 'alt': p[9]} for p in P], ensure_ascii=False)

''' + s[b:]

# ---- hero: the Bala Cinemas drone photo ----
rp('<img class="ab-hero-img" src="{{{{L:day.jpg}}}}" alt=""></div>\n  <span class="hl-ph ab-ph">Sample photo</span>',
   '<img class="ab-hero-img" src="{{{{L:real_bala_hero.jpg}}}}" alt=""></div>')
rp('<p class="ab-since"><span>Rooftop</span><span>Ground-mounted</span><span>Industrial</span><span>Residential</span></p>',
   '<p class="ab-since"><span>Showrooms</span><span>Cinemas</span><span>Commercial rooftops</span></p>')

# ---- work section: no filters (all four are commercial rooftops) ----
rp('<div><div class="eyebrow">Featured projects</div><h2 id="workTitle">From 20 kW homes to <em>1 MW plants</em></h2></div>\n      <p>Seven projects across rooftops, open land, factories, cinemas and homes. Choose one to read its story.</p>',
   '<div><div class="eyebrow">Featured projects</div><h2 id="workTitle">Rooftops we have <em>put to work</em></h2></div>\n      <p>Rooftop solar Sinelab has built for local businesses, photographed from the air. Choose a project to see it up close.</p>')
a = s.index('    <div class="pf-bar" role="group"'); b = s.index('    <ul class="pgrid" id="pgrid">')
s = s[:a] + s[b:]

# ---- the capacity chart waits until capacities are confirmed ----
a = s.index('<!-- ======= SCALE AT A GLANCE ======= -->'); b = s.index('<!-- ======= CALL TO ACTION ======= -->')
s = s[:a] + s[b:]
rp('From a single home to a megawatt plant, tell us what you have in mind', 'From a family home to a commercial rooftop, tell us what you have in mind')

# ---- dialog: real photo, no sample label; spec shows type, sector and status ----
rp('<div class="pd-img"><img id="pdImg" src="" alt=""><span class="hl-ph">Sample photo</span></div>', '<div class="pd-img"><img id="pdImg" src="" alt=""></div>')
rp('''        <div><dt>Capacity</dt><dd id="pdCap"></dd></div>
        <div id="pdLocRow"><dt>Location</dt><dd id="pdLoc"></dd></div>
        <div><dt>Type</dt><dd id="pdType2"></dd></div>''',
   '''        <div><dt>Type</dt><dd id="pdType2"></dd></div>
        <div><dt>Sector</dt><dd id="pdSector"></dd></div>''')
rp('''    $('pdName').textContent = p.name; $('pdCap').textContent = p.cap;
    $('pdLocRow').hidden = !p.loc; $('pdLoc').textContent = p.loc || '';''',
   '''    $('pdName').textContent = p.name; $('pdSector').textContent = p.sector; $('pdImg').style.objectPosition = p.focus;''')
rp(".pd-spec{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));", ".pd-spec{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));")
rp(".pd-spec #pdCap{font:300 30px/1 var(--f-display);letter-spacing:-0.04em}\n", "")
rp("  .pd-spec{grid-template-columns:1fr 1fr}\n", "")

# ---- card: an arrow in a circle where the capacity used to be ----
rp(".pc-cap{flex:none;", ".pc-go{flex:none;display:grid;place-items:center;width:46px;height:46px;border:1px solid var(--line);border-radius:50%;color:var(--ink);transition:background .4s,border-color .4s,transform .6s cubic-bezier(.2,.7,.2,1)}\n"
   ".pc-go svg{width:18px;height:18px}\n"
   ".pc-open:hover .pc-go,.pc-open:focus-visible .pc-go{background:var(--sun);border-color:var(--sun);transform:rotate(-45deg)}\n"
   ".pc-row{align-items:center}\n.pc-cap{flex:none;")
rp(".pd-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}",
   ".pd-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}\n.pd-img{min-height:clamp(420px,62svh,620px)}")
rp("  .pc-img img,.sc-bar i,.pd-body > *,.pd-img img{transition:none!important;transform:none!important;opacity:1}",
   "  .pc-img img,.sc-bar i,.pd-body > *,.pd-img img,.pc-go{transition:none!important;transform:none!important;opacity:1}")
open(p, 'w').write(s); print('patched')
