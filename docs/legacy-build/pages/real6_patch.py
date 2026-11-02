# 29 Oct: two more real projects from the user's drone DNGs – Palakkad Surgicals and Sinicon (capacities still left off).
import re
d = '/tmp/claude-0/site/'
def patch(fn, pairs):
    s = open(d + fn).read()
    for a, b in pairs:
        assert s.count(a) == 1, (fn, s.count(a), a[:90]); s = s.replace(a, b)
    open(d + fn, 'w').write(s); print('patched', fn)

# ---- Projects page ----
patch('projects.py', [
  ("""   'Drone view of the Jamal Sons building on a main road, with solar panels on its roof'),
]""", """   'Drone view of the Jamal Sons building on a main road, with solar panels on its roof'),
  ('palakkad-surgicals', 'Palakkad Surgicals', 'Manufacturing', 'real_psurg_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar for Palakkad Surgical Industries, with the panels on the roof of the block beside the main building.', None,
   'Drone view of the Palakkad Surgical Industries building, with solar panels on the roof of the smaller block'),
  ('sinicon', 'Sinicon', 'Industrial', 'real_sinicon_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar across the Sinicon factory: rows of panels on the sloped metal roof and more on the flat roof beside it.', None,
   'Drone view of the Sinicon factory, with rows of solar panels on its roofs'),
]"""),
  ('Rooftop solar projects by Sinelab Technologies for Bava Metals, Grand Bajaj Showroom, Bala Cinemas and Jamal Sons.',
   'Rooftop solar projects by Sinelab Technologies for Bava Metals, Grand Bajaj Showroom, Bala Cinemas, Jamal Sons, Palakkad Surgicals and Sinicon.'),
  ('<p class="ab-since"><span>Showrooms</span><span>Cinemas</span><span>Commercial rooftops</span></p>',
   '<p class="ab-since"><span>Factories</span><span>Showrooms</span><span>Cinemas</span></p>'),
  ('Rooftop solar Sinelab has built for local businesses, photographed from the air.',
   'Rooftop solar Sinelab has built for local businesses and factories, photographed from the air.'),
])

# ---- Homepage slider (run once on src_draft.html) ----
ART = lambda pid, name, img, alt, line, chips: f'''      <article class="proj"><div class="proj-img"><img src="{{{{L:{img}}}}}" alt="{alt}" loading="lazy"></div>
        <div class="proj-meta"><div><h3><a class="proj-a" href="projects.html#{pid}">{name}</a></h3><p class="loc">{line}</p></div></div>
        <div class="chips">{"".join(f"<span>{c}</span>" for c in chips)}</div></article>'''
s = open(d + 'src_draft.html').read()
a = '<div class="chips"><span>Rooftop solar</span><span>Commercial</span></div></article>\n    </div>\n    <div class="proj-progress"'
assert s.count(a) == 1
s = s.replace(a, '<div class="chips"><span>Rooftop solar</span><span>Commercial</span></div></article>\n'
  + ART('palakkad-surgicals', 'Palakkad Surgicals', 'real_psurg_slide.jpg', 'Drone view of the Palakkad Surgical Industries building, with solar panels on the roof of the smaller block',
        'Rooftop solar on the block beside the main factory building.', ['Rooftop solar', 'Manufacturing']) + '\n'
  + ART('sinicon', 'Sinicon', 'real_sinicon_slide.jpg', 'Drone view of the Sinicon factory, with rows of solar panels on its roofs',
        'Rows of panels across the factory’s sloped metal roof and flat roof.', ['Rooftop solar', 'Industrial'])
  + '\n    </div>\n    <div class="proj-progress"')
for x, y in [('<b id="projCount">01</b> / 04</span>', '<b id="projCount">01</b> / 06</span>'),
             ('<p>Rooftop solar Sinelab has built for local businesses, photographed from the air.</p>', '<p>Rooftop solar Sinelab has built for local businesses and factories, photographed from the air.</p>')]:
    assert s.count(x) == 1, x; s = s.replace(x, y)
open(d + 'src_draft.html', 'w').write(s); print('patched src_draft.html')

# ---- Gallery ----
patch('gallery.py', [
  ("        ('installations', 'real_jamal.jpg', 'Jamal Sons, rooftop solar on a main road', 's')]",
   "        ('installations', 'real_jamal.jpg', 'Jamal Sons, rooftop solar on a main road', 's'),\n"
   "        ('installations', 'real_psurg.jpg', 'Palakkad Surgicals, panels on the side block', 'w'),\n"
   "        ('installations', 'real_sinicon.jpg', 'Sinicon, panels across the factory roofs', 'w')]"),
  ("FOCUS = {'real_bava.jpg': '30% 50%'}", "FOCUS = {'real_bava.jpg': '30% 50%', 'real_psurg.jpg': '40% 50%', 'real_sinicon.jpg': '62% 50%'}"),
  ("      ('real_jamal_card.jpg', 'Jamal Sons', 'Rooftop solar · Commercial', 'Rooftop solar for a commercial building on a busy main road.')]",
   "      ('real_jamal_card.jpg', 'Jamal Sons', 'Rooftop solar · Commercial', 'Rooftop solar for a commercial building on a busy main road.'),\n"
   "      ('real_psurg_card.jpg', 'Palakkad Surgicals', 'Rooftop solar · Manufacturing', 'Panels on the roof of the block beside the main factory building.'),\n"
   "      ('real_sinicon_card.jpg', 'Sinicon', 'Rooftop solar · Industrial', 'Rows of panels across the factory’s sloped metal roof and flat roof.')]"),
  (".gm-real{columns:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 clamp(14px,1.6vw,22px);",
   ".gm-real{columns:auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(22px,2.4vw,34px) clamp(14px,1.6vw,22px);"),
  (".gm-real .gt .gt-img{aspect-ratio:4/5}", ".gm-real .gt .gt-img{aspect-ratio:4/3}"),
  ("The first four photos are Sinelab projects.", "The first six photos are Sinelab projects."),
])
