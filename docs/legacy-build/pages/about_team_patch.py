# About: six people no longer squeeze into one expanding row (user, 29 Oct: "layout is not nice").
# New layout: the two co-founders as large side-by-side cards with photo + bio, then the other four in a row of
# equal cards (photo, name, role, bio). Static content: no hover-to-open, nothing to tab to.
p = '/tmp/claude-0/site/about.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

a = s.index("leaders = '<div class=\"leaders ab-leaders\">"); b = s.index("+ '\\n    </div>\\n'", a) + len("+ '\\n    </div>\\n'")
s = s[:a] + '''def tm_card(n, r, g, b, big):
    tbc = ' tbc' if 'to be confirmed' in r else ''
    bio = f'<p class="tm-bio">{b}</p>' if b else ''
    return f\'\'\'        <article class="tm-card{" tm-lg" if big else ""}">
          <div class="tm-ph">{SIL}<span class="ab-ld-tag">{g}</span></div>
          <div class="tm-body"><h3>{n}</h3><p class="tm-role{tbc}">{r}</p>{bio}</div>
        </article>\'\'\'
founders = [t for t in TEAM if t[2] == 'Co-founder']; others = [t for t in TEAM if t[2] != 'Co-founder']
leaders = ('<div class="tm">\\n      <div class="tm-founders">\\n' + '\\n'.join(tm_card(*t, True) for t in founders) + '\\n      </div>\\n'
           + '      <div class="tm-team">\\n' + '\\n'.join(tm_card(*t, False) for t in others) + '\\n      </div>\\n    </div>\\n')''' + s[b:]

rp("'.leader, .ab-site, .ab-award, .ab-vm-item, .ab-pr li, .ab-story-body > p'", "'.tm-card, .ab-site, .ab-award, .ab-vm-item, .ab-pr li, .ab-story-body > p'")
rp("+ js_core + js_nav + js_reveal + js_leaders + JS +", "+ js_core + js_nav + js_reveal + JS +")

rp("/* About: six people (founders, leadership, team) with short bios */", """/* About: team – two co-founders large, then four equal cards */
.tm{display:grid;gap:clamp(36px,4vw,56px)}
.tm-founders{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(14px,1.6vw,22px)}
.tm-team{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(18px,2vw,28px)}
.tm-card{position:relative;min-width:0}
.tm-ph{position:relative;display:grid;place-items:end center;aspect-ratio:1/1;border-radius:18px;overflow:hidden;background:linear-gradient(170deg,#EFEFF2,#CDCDD3);color:#A7A7AF}
.tm-ph svg{width:62%;margin-bottom:-7%;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.tm-card:hover .tm-ph svg{transform:translateY(-4px) scale(1.03)}
.tm-ph .ab-ld-tag{right:12px;top:12px}
.tm-body{padding:18px 2px 0}
.tm-card h3{margin:0;font-size:clamp(19px,1.5vw,22px);font-weight:500;letter-spacing:-0.015em;line-height:1.2;color:var(--ink)}
.tm-role{margin:6px 0 0;font:500 12.5px var(--f-mono);letter-spacing:.04em;text-transform:uppercase;color:var(--accent-ink)}
.tm-role.tbc{text-transform:none;letter-spacing:0;font-family:var(--f-body);font-size:14px;font-style:italic;color:var(--muted)}
.tm-bio{margin:12px 0 0;padding-top:12px;border-top:1px solid var(--line);font-size:15px;line-height:1.6;color:var(--muted)}
.tm-lg{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1fr);border-radius:22px;background:var(--paper);overflow:hidden}
.tm-lg .tm-ph{aspect-ratio:auto;min-height:clamp(300px,26vw,380px);border-radius:0}
.tm-lg .tm-body{display:flex;flex-direction:column;justify-content:flex-end;padding:clamp(22px,2.4vw,34px)}
.tm-lg h3{font-size:clamp(24px,2.1vw,32px);font-weight:400;letter-spacing:-0.03em}
.tm-lg .tm-bio{font-size:15.5px}
@media (max-width:1100px){
  .tm-founders{grid-template-columns:1fr}
  .tm-team{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:34px}
}
@media (max-width:600px){
  /* phones (user asked for vertical cards): founders photo-on-top; the other four as a simple list */
  .tm-lg{grid-template-columns:1fr}
  .tm-lg .tm-ph{min-height:0;height:220px}
  .tm-lg .tm-body{padding:20px 20px 22px}
  .tm-team{grid-template-columns:1fr;row-gap:0}
  .tm-team .tm-card{display:grid;grid-template-columns:88px minmax(0,1fr);column-gap:16px;align-items:center;padding:18px 0;border-top:1px solid var(--line)}
  .tm-team .tm-card:last-child{border-bottom:1px solid var(--line)}
  .tm-team .tm-ph{border-radius:14px}
  .tm-team .tm-ph .ab-ld-tag{display:none}
  .tm-team .tm-body{padding:0}
  .tm-team .tm-bio{grid-column:1/-1}
  .tm-team .tm-card{grid-template-areas:"ph body" "bio bio"}
}
@media (prefers-reduced-motion: reduce){.tm-ph svg{transition:none}.tm-card:hover .tm-ph svg{transform:none}}
/* (older single-row styles below no longer match anything) */""")
open(p, 'w').write(s); print('patched')
