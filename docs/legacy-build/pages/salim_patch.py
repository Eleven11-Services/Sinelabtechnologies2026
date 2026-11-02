# 29 Oct: the user's top-down drone photo of "Salim Hybrid Residence" (the content doc's Saleem Residence, 20 kW hybrid)
# becomes project 07 on Projects, the homepage slider and the Gallery. Capacity still left off.
d = '/tmp/claude-0/site/'
def patch(fn, pairs):
    s = open(d + fn).read()
    for a, b in pairs:
        assert s.count(a) == 1, (fn, s.count(a), a[:90]); s = s.replace(a, b)
    open(d + fn, 'w').write(s); print('patched', fn)
SUM = 'A residential hybrid solar solution combining clean generation with battery-backed functionality, designed around the household’s energy needs.'
ALT = 'Top-down drone view of the Salim residence, with solar panels on two of its flat roofs'
patch('projects.py', [
  ("""   'Drone view of the Sinicon factory, with rows of solar panels on its roofs'),
]""", f"""   'Drone view of the Sinicon factory, with rows of solar panels on its roofs'),
  ('salim-residence', 'Salim Hybrid Residence', 'Residential', 'real_salim_card.jpg', '50% 50%', 'Hybrid solar', None,
   '{SUM}', None,
   '{ALT}'),
]"""),
  ('Jamal Sons, Palakkad Surgicals and Sinicon.', 'Jamal Sons, Palakkad Surgicals, Sinicon and Salim Hybrid Residence.'),
  ('<p class="ab-since"><span>Factories</span><span>Showrooms</span><span>Cinemas</span></p>', '<p class="ab-since"><span>Factories</span><span>Showrooms</span><span>Homes</span></p>'),
  ('Rooftop solar Sinelab has built for local businesses and factories, photographed from the air.', 'Solar Sinelab has built for businesses, factories and homes, photographed from the air.'),
])
s = open(d + 'src_draft.html').read()
a = "<div class=\"chips\"><span>Rooftop solar</span><span>Industrial</span></div></article>\n    </div>\n    <div class=\"proj-progress\""
assert s.count(a) == 1
s = s.replace(a, """<div class="chips"><span>Rooftop solar</span><span>Industrial</span></div></article>
      <article class="proj"><div class="proj-img"><img src="{{L:real_salim_slide.jpg}}" alt=\"""" + ALT + """\" loading="lazy"></div>
        <div class="proj-meta"><div><h3><a class="proj-a" href="projects.html#salim-residence">Salim Hybrid Residence</a></h3><p class="loc">Hybrid solar with battery backup, designed around a family home.</p></div></div>
        <div class="chips"><span>Hybrid solar</span><span>Residential</span></div></article>
    </div>
    <div class="proj-progress\"""")
for x, y in [('<b id="projCount">01</b> / 06</span>', '<b id="projCount">01</b> / 07</span>'),
             ('<p>Rooftop solar Sinelab has built for local businesses and factories, photographed from the air.</p>', '<p>Solar Sinelab has built for businesses, factories and homes, photographed from the air.</p>')]:
    assert s.count(x) == 1, x; s = s.replace(x, y)
open(d + 'src_draft.html', 'w').write(s); print('patched src_draft.html')
patch('gallery.py', [
  ("        ('installations', 'real_sinicon.jpg', 'Sinicon, panels across the factory roofs', 'w')]",
   "        ('installations', 'real_sinicon.jpg', 'Sinicon, panels across the factory roofs', 'w'),\n"
   "        ('installations', 'real_salim.jpg', 'Salim Hybrid Residence, panels on the flat roofs', 'w')]"),
  ("      ('real_sinicon_card.jpg', 'Sinicon', 'Rooftop solar · Industrial', 'Rows of panels across the factory’s sloped metal roof and flat roof.')]",
   "      ('real_sinicon_card.jpg', 'Sinicon', 'Rooftop solar · Industrial', 'Rows of panels across the factory’s sloped metal roof and flat roof.'),\n"
   "      ('real_salim_card.jpg', 'Salim Hybrid Residence', 'Hybrid solar · Residential', 'Hybrid solar with battery backup, designed around a family home.')]"),
  (".gm-real{columns:auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));", ".gm-real{columns:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));"),
])
