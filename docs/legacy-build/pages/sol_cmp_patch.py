p = '/tmp/claude-0/site/solutions.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80]); s = s.replace(a, b)

rp("""STEPS = [('Assess',""", """# phones (user: "make it easy for mobile, visually"): one card per system instead of the table
CI_GRID = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 7 22M12 2l5 20M8.5 15h7M9.6 10.5h4.8M5 6h14M10.7 6 12 2l1.3 4"/></svg>'
CI_BATT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="16" height="10" rx="2"/><path d="M19 10h2v4h-2M11.5 9 9 12.5h4l-2.5 3.5"/></svg>'
CI_PLUG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/></svg>'
CI_SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>'
CHK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>'
DASH = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 8h8"/></svg>'
SYSTEMS = [('On-grid', CI_GRID, ['yes', 'no', 'no'], 'Sent to the grid through a net meter', 'Lower bills'),
           ('Off-grid', CI_BATT, ['no', 'yes', 'yes'], 'Stored in the battery', 'Remote sites, farms and estates'),
           ('Hybrid', CI_SUN, ['yes', 'yes', 'part'], 'Battery first, then the grid', 'Savings with backup')]
FEATS = [('Grid', CI_GRID), ('Battery', CI_BATT), ('Power-cut backup', CI_PLUG)]
def feat(lbl, ic, st):
    word = {'yes': 'Yes', 'no': 'No', 'part': 'Selected loads'}[st]
    return (f'<li class="ccf is-{st}"><span class="ccf-ico">{ic}</span><span class="ccf-l">{lbl}</span>'
            f'<span class="ccf-s">{DASH if st == "no" else CHK}{word}</span></li>')
cmp_cards = '\\n'.join(f'''      <article class="cc">
        <div class="cc-head"><span class="cc-ico">{ic}</span><div><h3>{name}</h3><p class="cc-best">Best for {best[0].lower() + best[1:]}</p></div></div>
        <ul class="cc-feats">{"".join(feat(l, fi, st) for (l, fi), st in zip(FEATS, sts))}</ul>
        <p class="cc-extra"><span>Extra solar power</span>{extra}</p>
      </article>''' for name, ic, sts, extra, best in SYSTEMS)

STEPS = [('Assess',""")
rp("""    <a class="text-link" href="index.html#anatomy">See how each one works""", """    <div class="cmp-cards">
{cmp_cards}
    </div>
    <a class="text-link" href="index.html#anatomy">See how each one works""")
# phone styles: hide the table, show the cards
a = s.index("@media (max-width:700px){\n  .cmp-wrap{overflow:visible}")
b = s.index("  .cmp-n i::after{left:4px;right:4px;top:7px}\n}\n", a) + len("  .cmp-n i::after{left:4px;right:4px;top:7px}\n}\n")
s = s[:a] + """.cmp-cards{display:none}
@media (max-width:700px){
  .cmp-wrap{display:none}
  .cmp-cards{display:grid;gap:14px}
  .cc{padding:20px 18px;border-radius:20px;background:#fff}
  .cc-head{display:flex;align-items:center;gap:14px}
  .cc-ico{display:grid;place-items:center;flex:none;width:52px;height:52px;border-radius:50%;background:var(--navy-deep);color:var(--sun)}
  .cc-ico svg{width:26px;height:26px}
  .cc h3{margin:0;font-size:26px;font-weight:400;letter-spacing:-0.025em;line-height:1.1;color:var(--ink)}
  .cc-best{display:inline-flex;align-items:center;gap:7px;margin:6px 0 0;font-size:14.5px;color:var(--ink)}
  .cc-best::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--sun)}
  .cc-feats{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
  .ccf{display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 6px 13px;border-radius:14px;background:var(--paper);text-align:center}
  .ccf-ico{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:#55555D}
  .ccf-ico svg{width:19px;height:19px}
  .ccf-l{font-size:13px;line-height:1.25;color:var(--ink)}
  .ccf-s{display:inline-flex;align-items:center;gap:4px;font-size:12.5px;font-weight:600;color:#55555D}
  .ccf-s svg{width:14px;height:14px}
  .ccf.is-yes,.ccf.is-part{background:#FFF4D4}
  .ccf.is-yes .ccf-ico,.ccf.is-part .ccf-ico{background:var(--sun);color:var(--ink)}
  .ccf.is-yes .ccf-s,.ccf.is-part .ccf-s{color:var(--ink)}
  .cc-extra{display:flex;flex-direction:column;gap:4px;margin:16px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:15.5px;color:var(--ink)}
  .cc-extra span{font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
}
""" + s[b:]
open(p, 'w').write(s); print('patched')
