# Gallery: Sinelab's own drone photos (29 Oct). The highlights deck shows the four real projects; the grid opens with
# their full photos (no sample label), followed by the labelled sample photos until more of Sinelab's own arrive.
p = '/tmp/claude-0/site/gallery.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

# real photos first, with their own shapes; samples keep the old rhythm after them
rp("ITEMS = [it for it in ITEMS if it[1]]          # user: show only the photos we already have (the shot list stays in the notes)\n"
   "SHAPES = ['w', 's', 't', 'w', 't', 's', 'w', 's', 't', 'w']\n"
   "ITEMS = [(c, i, t, SHAPES[k % len(SHAPES)]) for k, (c, i, t, _) in enumerate(ITEMS)]",
   "ITEMS = [it for it in ITEMS if it[1]]          # user: show only the photos we already have (the shot list stays in the notes)\n"
   "SHAPES = ['w', 's', 't', 'w', 't', 's', 'w', 's', 't', 'w']\n"
   "ITEMS = [(c, i, t, SHAPES[(k + 4) % len(SHAPES)]) for k, (c, i, t, _) in enumerate(ITEMS)]\n"
   "REAL = [('installations', 'real_bala.jpg', 'Bala Cinemas, rooftop solar from the air', 't'),\n"
   "        ('installations', 'real_bava.jpg', 'Bava Metals, panels along the metal roofs', 'w'),\n"
   "        ('installations', 'real_bajaj.jpg', 'Grand Bajaj Showroom, array on a raised frame over the terrace', 't'),\n"
   "        ('installations', 'real_jamal.jpg', 'Jamal Sons, rooftop solar on a main road', 's')]\n"
   "REAL_IMGS = {it[1] for it in REAL}\n"
   "ITEMS = REAL + ITEMS")
rp("""        inner = f'<img src="{{{{L:{img}}}}}" data-g="{img}" alt="" loading="lazy"><span class="hl-ph">Sample photo</span>'""",
   """        inner = f'<img src="{{{{L:{img}}}}}" data-g="{img}" alt="" loading="lazy">' + ('' if img.startswith('real_') else '<span class="hl-ph">Sample photo</span>')""")
rp("DATA = json.dumps([{'cat': CNAME[c].replace('&amp;', '&'), 'title': t, 'img': bool(i), 'icon': c} for c, i, t, _ in ITEMS], ensure_ascii=False)",
   "DATA = json.dumps([{'cat': CNAME[c].replace('&amp;', '&'), 'title': t, 'img': bool(i), 'real': bool(i and i.startswith('real_')), 'icon': c} for c, i, t, _ in ITEMS], ensure_ascii=False)")

# highlights deck: the four real projects (card crops, loaded directly)
a = s.index("# highlights deck: the top card flips over"); b = s.index("NH = len(HL)")
s = s[:a] + """# highlights deck: Sinelab's four real projects, slid sideways one after another
HL = [('real_bala_card.jpg', 'Bala Cinemas', 'Rooftop solar · Cinema', 'Enphase microinverters handle shading on a challenging roof.'),
      ('real_bajaj_card.jpg', 'Grand Bajaj Showroom', 'Rooftop solar · Showroom', 'Panels on a raised steel frame above the flat terrace.'),
      ('real_bava_card.jpg', 'Bava Metals', 'Rooftop solar · Commercial', 'Panels set along the metal roofs of a busy town-centre building.'),
      ('real_jamal_card.jpg', 'Jamal Sons', 'Rooftop solar · Commercial', 'Rooftop solar for a commercial building on a busy main road.')]
""" + s[b:]
rp('''            <div class="hc-f"><img data-g="{im}" alt=""><i class="hc-shade"></i><span class="hl-ph">Sample photo</span></div>''',
   '''            <div class="hc-f"><img src="{{{{L:{im}}}}}" alt=""{' loading="lazy"' if i else ''}><i class="hc-shade"></i></div>''')

# viewer: real photos get a plain description and no sample label
rp("if (g.img){ const src = opens[k].querySelector('img').src; $('lbImg').src = src; $('lbImg').alt = 'Sample photo: ' + g.title; }",
   "lb.classList.toggle('is-real', !!g.real);\n    if (g.img){ const src = opens[k].querySelector('img').src; $('lbImg').src = src; $('lbImg').alt = (g.real ? '' : 'Sample photo: ') + g.title; }")
rp(".lb.is-ph .lb-stage img,.lb.is-ph #lbSample{display:none}", ".lb.is-ph .lb-stage img,.lb.is-ph #lbSample,.lb.is-real #lbSample{display:none}")
rp("<p class=\"gl-note\">Photos marked “Sample photo” are placeholders, not Sinelab projects. Sinelab’s own photographs and drone footage will replace them.</p>",
   "<p class=\"gl-note\">The first four photos are Sinelab projects. Photos marked “Sample photo” are placeholders, not Sinelab work, and will be replaced as more of Sinelab’s own photographs arrive.</p>")
open(p, 'w').write(s); print('patched')
