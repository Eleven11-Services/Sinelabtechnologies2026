# Step 17 (29 Oct): homepage uses Sinelab's own drone photos of four real projects (user: "update the proj images now the real proj images").
# Capacities are left off for now. Runs once on src_draft.html (backup: src_v51_pre_real.html).
d = '/tmp/claude-0/site/'
s = open(d + 'src_draft.html').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, ('COUNT', s.count(a), a[:100]); s = s.replace(a, b)

# ---- featured projects slider: four real projects ----
a = s.index('      <article class="proj"><div class="proj-img"><img src="{{L:pj_drone.jpg}}"')
b = s.index('    </div>\n    <div class="proj-progress"')
PJ = [('bava-metals', 'Bava Metals', 'real_bava_slide.jpg', 'Drone view of the Bava Metals building, with solar panels along its metal roofs',
       'Rooftop solar set along the metal roofs of a busy town-centre building.', ['Rooftop solar', 'Commercial']),
      ('grand-bajaj', 'Grand Bajaj Showroom', 'real_bajaj_slide.jpg', 'Solar panels on a raised steel frame above the Grand Bajaj showroom',
       'Panels on a raised steel frame above the showroom’s flat terrace.', ['Rooftop solar', 'Showroom']),
      ('bala-cinemas', 'Bala Cinemas', 'real_bala_slide.jpg', 'Drone view of the Bala Cinemas building with a solar array on its roof',
       'Rooftop installation with Enphase microinverters to handle site-specific shading.', ['Rooftop solar', 'Completed']),
      ('jamal-sons', 'Jamal Sons', 'real_jamal_slide.jpg', 'Drone view of the Jamal Sons building on a main road, with solar panels on its roof',
       'Rooftop solar for a commercial building on a busy main road.', ['Rooftop solar', 'Commercial'])]
s = s[:a] + '\n'.join(f'''      <article class="proj"><div class="proj-img"><img src="{{{{L:{img}}}}}" alt="{alt}" loading="lazy"></div>
        <div class="proj-meta"><div><h3><a class="proj-a" href="projects.html#{pid}">{name}</a></h3><p class="loc">{line}</p></div></div>
        <div class="chips">{"".join(f"<span>{c}</span>" for c in chips)}</div></article>''' for pid, name, img, alt, line, chips in PJ) + '\n' + s[b:]
rep('<b id="projCount">01</b> / 06</span>', '<b id="projCount">01</b> / 04</span>')
rep('<p>A selection of rooftop, ground-mounted, industrial and residential solar work.</p>',
    '<p>Rooftop solar Sinelab has built for local businesses, photographed from the air.</p>')
rep('.proj-meta .save{text-align:right}', '.proj-meta .save{text-align:right}\n'
    '.proj-a{color:inherit;text-decoration:underline;text-decoration-color:transparent;text-decoration-thickness:2px;text-underline-offset:6px;transition:text-decoration-color .3s}\n'
    '.proj-a:hover,.proj-a:focus-visible{text-decoration-color:var(--sun)}')

# ---- gallery panel 01 (Solar installations): a real photo instead of the drawing ----
rep('''      <article class="ga is-on" tabindex="0" aria-expanded="true" aria-label="Solar installations">
        <div class="hl-art art-roof"><i class="field"></i></div>''',
    '''      <article class="ga is-on" tabindex="0" aria-expanded="true" aria-label="Solar installations">
        <div class="hl-art"><img class="ga-photo" src="{{L:real_bala_card.jpg}}" alt="" loading="lazy"><i class="ga-shade"></i></div>''')
i = s.index('aria-label="Solar installations">'); j = s.index('<span class="hl-ph">Photos to be added</span>\n', i)
assert j - i < 1600; s = s[:j] + s[j + len('<span class="hl-ph">Photos to be added</span>\n'):]
s = s[:j].rstrip(' ') + s[j:].lstrip(' ') if False else s
rep('<p>Sample layout. Original photographs and drone footage will fill each category.</p>',
    '<p>Installation photos are Sinelab’s own. Photos for the other categories will be added soon.</p>')
rep('.ga .hl-ph{opacity:0;transition:opacity .4s}',
    '.hl-art .ga-photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}\n'
    '.hl-art .ga-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(9,9,11,.05) 30%,rgba(9,9,11,.82) 100%)}\n'
    '.ga .hl-ph{opacity:0;transition:opacity .4s}')
open(d + 'src_draft.html', 'w').write(s); print('step 17 ok')
