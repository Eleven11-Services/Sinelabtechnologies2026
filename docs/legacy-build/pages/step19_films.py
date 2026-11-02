# Step 19 (29 Oct): "Projects in motion" now features the user's two milestone projects, Palakkad Surgicals and Sinicon
# (user: "update here the palakkad surgicals and sinicon as milestones"). No drone video yet, so each clip is a slow
# push-in made from the real aerial photo (/tmp/claude-0/films2/mk.py). The sample clips are gone.
d = '/tmp/claude-0/site/'
s = open(d + 'src_draft.html').read()
a = s.index('<!-- ======= PROJECT FILMS ======= -->'); b = s.index('<!-- ======= WHY SINELAB ======= -->')
F = [('psurg', 'Palakkad Surgicals', 'Rooftop solar · Manufacturing', 'Powering <em>Palakkad’s industry.</em>',
      'Rooftop solar for Palakkad Surgical Industries, on the roof of the block beside the main building.',
      'Aerial photo of the Palakkad Surgical Industries building, slowly zooming in on its rooftop solar panels'),
     ('sinicon', 'Sinicon', 'Rooftop solar · Industrial', 'Every roof, <em>put to work.</em>',
      'Rows of panels across the factory’s sloped metal roof, with more on the flat roof beside it.',
      'Aerial photo of the Sinicon factory, slowly zooming in on the rows of solar panels on its roofs')]
n = len(F)
slides = '\n'.join(f'''      <article class="film{" is-on" if k == 0 else ""}" aria-roledescription="slide" aria-label="{k + 1} of {n}"{"" if k == 0 else ' aria-hidden="true"'}>
        <video muted playsinline preload="none" poster="{{{{L:film_{key}.jpg}}}}" data-src="media/{key}.mp4" aria-label="{alt}"></video>
        <div class="film-copy">
          <span class="film-kick">Milestone · {name}</span>
          <h3>{h3}</h3>
          <p>{line}</p>
        </div>
      </article>''' for k, (key, name, kind, h3, line, alt) in enumerate(F))
tabs = '\n'.join(f'''      <button type="button"{' class="on"' if k == 0 else ''} aria-current="{"true" if k == 0 else "false"}"><img src="{{{{L:film_{key}_t.jpg}}}}" alt=""><span><b>{name}</b><small>{kind}</small></span><i><b></b></i></button>'''
                 for k, (key, name, kind, h3, line, alt) in enumerate(F))
old = s[a:b]
i = old.index('<button type="button" class="film-play"'); j = old.index('</button>', i) + len('</button>')
play = old[i:j]
link = old[old.index('      <a class="text-link" href="#projects">'):old.index('</a>', old.index('<a class="text-link" href="#projects">')) + 4]
new = f'''<!-- ======= PROJECT FILMS ======= -->
<section class="films band" id="films" aria-labelledby="filmsTitle" aria-roledescription="carousel">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Projects in motion</div><h2 id="filmsTitle">Milestone projects, <em>from above</em></h2></div>
      <p>Two industrial rooftops that mark Sinelab’s growth, seen from the air.</p>
    </div>
    <div class="film-stage" id="filmStage">
{slides}
      {play}
    </div>
    <div class="film-foot">
      <div class="film-tabs" id="filmTabs">
{tabs}
      </div>
{link.replace('href="#projects"', 'href="projects.html"').replace('All featured projects', 'All projects')}
    </div>
  </div>
</section>

'''
s = s[:a] + new + s[b:]
open(d + 'src_draft.html', 'w').write(s); print('step 19 ok')
