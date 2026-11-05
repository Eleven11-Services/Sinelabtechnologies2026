# Builds the Netlify-ready multi-page site from the current draft sources:
# index (src_draft.html), about, solutions, projects, gallery, contact (*_src.html).
# Real files instead of inlined images, self-hosted libraries and fonts, a proper <head> per page,
# working Netlify Forms on the homepage and Contact page, cache headers, and a zip for Netlify Drop.
import re, shutil, os, json, sys
sys.path.insert(0, '/tmp/claude-0/site'); from webp_cache import webp   # every image ships as WebP
from PIL import Image
d = '/tmp/claude-0/site/'
OUT = '/tmp/claude-0/deploy/sinelab-website/'
F = '/tmp/claude-0/fonts/manrope/'
L = '/tmp/claude-0/libs/'
shutil.rmtree(OUT, ignore_errors=True)
for sub in ['assets/img', 'assets/fonts', 'assets/js', 'media']:
    os.makedirs(OUT + sub, exist_ok=True)

PAGES = [('index.html', 'src_draft.html', 'Sinelab Technologies | Solar, Energy Storage & Lighting Solutions'),
         ('about.html', 'about_src.html', None), ('solutions.html', 'solutions_src.html', None),
         ('projects.html', 'projects_src.html', None), ('gallery.html', 'gallery_src.html', None),
         ('contact.html', 'contact_src.html', None)]

LIBS = {
  'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js': (L + 'gsap-3.12.5/package/dist/gsap.min.js', 'gsap.min.js'),
  'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js': (L + 'gsap-3.12.5/package/dist/ScrollTrigger.min.js', 'ScrollTrigger.min.js'),
  'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js': (L + 'three-0.128.0/package/build/three.min.js', 'three.min.js'),
  'https://unpkg.com/lenis@1.1.13/dist/lenis.min.js': (L + 'lenis-1.1.13/package/dist/lenis.min.js', 'lenis.min.js'),
}
RANGES = {
  'latin': 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
  'latin-ext': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
}
faces = []
for w in (300, 400, 500, 600, 700):
    for sub, rng in RANGES.items():
        fn = f'manrope-{sub}-{w}-normal.woff2'
        shutil.copy(F + fn, OUT + 'assets/fonts/' + fn)
        faces.append(f"@font-face{{font-family:'Manrope';font-style:normal;font-display:swap;font-weight:{w};src:url(assets/fonts/{fn}) format('woff2');unicode-range:{rng}}}")
FONT_HEAD = ('<link rel="preload" href="assets/fonts/manrope-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<style>' + ''.join(faces) + '</style>')
OLD_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap">'''
DEFAULT_DESC = 'Sinelab Technologies is a Kerala-rooted engineering and manufacturing company delivering solar, energy storage and lighting solutions for homes, businesses and industries.'

def rp(s, a, b, label):
    assert s.count(a) == 1, (label, s.count(a), a[:70]); return s.replace(a, b)

# ---- live form sending (Netlify Forms). The review previews only showed a thank-you. ----
SEND = """fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(FORM)).toString() })"""
def live_forms(name, s):
    if name == 'index.html':
        s = rp(s, '<form class="enq" id="enqForm" novalidate>',
               '<form class="enq" id="enqForm" name="homepage-enquiry" method="post" data-netlify="true" netlify-honeypot="bot-field" novalidate>\n'
               '      <input type="hidden" name="form-name" value="homepage-enquiry">\n'
               '      <p style="position:absolute;left:-9999px" aria-hidden="true"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>', name)
        s = rp(s, 'Thanks. In the live site this sends your details to info@sinelabtechnologies.com and the team will get back to you.',
               'Thank you! We have your enquiry and our team will call you back soon.', name)
        s = rp(s, """  if (bad.length){ bad[0].focus(); return; }
  document.getElementById('formOk').hidden = false;""",
               """  if (bad.length){ err.textContent = 'Please add your name and phone number so we can call you back.'; bad[0].focus(); return; }
  const FORM = e.target, btn = FORM.querySelector('button[type=submit]'); btn.disabled = true;
  """ + SEND + """
    .then(r => { if (!r.ok) throw new Error(r.status); document.getElementById('formOk').hidden = false; FORM.reset(); })
    .catch(() => { err.textContent = 'Sorry, your enquiry did not send. Please call or WhatsApp us on +91 99462 07738.'; err.hidden = false; })
    .finally(() => { btn.disabled = false; });""", name)
    if name == 'contact.html':
        s = rp(s, '      <p class="cf-ok-note">Preview only: on the live site this sends your details to info@sinelabtechnologies.com.</p>\n', '', name)
        s = rp(s, """    form.hidden = true; ok.hidden = false; ok.focus();""",
               """    const FORM = form, btn = form.querySelector('button[type=submit]'); btn.disabled = true;
    """ + SEND + """
      .then(r => { if (!r.ok) throw new Error(r.status); form.hidden = true; ok.hidden = false; ok.focus(); })
      .catch(() => { sum.textContent = 'Sorry, your enquiry did not send. Please call or WhatsApp us on +91 99462 07738.'; sum.hidden = false; sum.focus && sum.focus(); })
      .finally(() => { btn.disabled = false; });""", name)
    return s

used_all = set()
for out_name, src_name, title in PAGES:
    s = open(d + src_name).read()
    # images
    used = set(re.findall(r'\{\{L:([^}]+)\}\}', s)); used_all |= used
    s = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: 'assets/img/' + os.path.splitext(m.group(1))[0] + '.webp', s)
    for key, src, dst in [('{{LOGO_BLACK}}', 'logo_black.png', 'logo-black.webp'), ('{{LOGO}}', 'logo.png', 'logo.webp'),
                          ('{{LOGO_WHITE}}', 'logo_white.png', 'logo-white.webp'), ('{{ABOUT_IMG}}', 'about.jpg', 'about.webp')]:
        if key in s:
            shutil.copy(webp(d + src), OUT + 'assets/img/' + dst); s = s.replace(key, 'assets/img/' + dst)
    s = re.sub(r'<img (?![^>]*decoding=)', '<img decoding="async" ', s)   # decode images off the main thread
    assert not re.search(r'\{\{[A-Z_]+[:}]', s), (out_name, re.findall(r'\{\{[^}]+\}\}', s)[:3])
    # libraries
    for url, (src, nm) in LIBS.items():
        if url in s:
            shutil.copy(src, OUT + 'assets/js/' + nm)
            s = s.replace(f'<script src="{url}"></script>', f'<script src="assets/js/{nm}"></script>')
    assert 'cdnjs.cloudflare.com' not in s and 'unpkg.com' not in s, out_name
    # fonts
    s = rp(s, OLD_FONTS, FONT_HEAD, out_name)
    # head
    t = re.search(r'<title>([^<]*)</title>', s); page_title = title or (t.group(1) if t else 'Sinelab Technologies')
    m = re.search(r'<meta name="description" content="([^"]*)">', s); desc = m.group(1) if (m and out_name != 'index.html') else DEFAULT_DESC
    s = re.sub(r'<title>[^<]*</title>\n?', '', s)
    s = re.sub(r'<meta name="description" content="[^"]*">\n?', '', s)
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    s = live_forms(out_name, s)
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{page_title.replace('&', '&amp;').replace('&amp;amp;', '&amp;')}</title>
<meta name="description" content="{desc}">
<!-- Review build with sample photos: keeps search engines out. Delete this line when the site goes live on the real domain. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#09090B">
<meta property="og:title" content="{page_title.replace('&', '&amp;').replace('&amp;amp;', '&amp;')}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/og.jpg">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
'''
    cut = s.index('<!-- ======= NAV ======= -->')
    s = head + s[:cut].strip() + '\n</head>\n<body>\n' + s[cut:] + '\n</body>\n</html>\n'
    open(OUT + out_name, 'w').write(s)
    print(f'{out_name:16} {os.path.getsize(OUT + out_name) // 1024:4d} KB  {len(used)} images  "{page_title}"')

for f in sorted(used_all):
    shutil.copy(webp(d + 'layers/' + f), OUT + 'assets/img/' + os.path.splitext(f)[0] + '.webp')
shutil.copy(d + 'og.jpg', OUT + 'assets/img/og.jpg')   # social share image: real Bala Cinemas drone photo, 1200x630
# favicon from the logo mark
mark = Image.open('/tmp/claude-0/brand/pack/01_Logo/sinelab-app-icon-512.png').convert('RGBA')
mark.resize((180, 180), Image.LANCZOS).save(OUT + 'assets/img/apple-touch-icon.png')
mark.resize((64, 64), Image.LANCZOS).save(OUT + 'favicon.png')
for f in os.listdir(d + 'media'):
    shutil.copy(d + 'media/' + f, OUT + 'media/' + f)

open(OUT + '_headers', 'w').write('''/assets/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400
/media/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
''')
open(OUT + 'README.txt', 'w').write('''SINELAB TECHNOLOGIES WEBSITE (review build for Netlify)

Pages: index.html (home), about.html, solutions.html, projects.html, gallery.html, contact.html
assets/img    images (sample photos until Sinelab's own arrive)
assets/js     animation libraries (GSAP, ScrollTrigger, Three.js, Lenis)
assets/fonts  Manrope
media         project films (sample footage)
_headers      Netlify caching and security headers

Forms: the homepage form ("homepage-enquiry") and the Contact page form ("enquiry") send to Netlify Forms.
In Netlify: Forms > Enable form detection, then redeploy; add an email notification to info@sinelabtechnologies.com.

Before launch on the real domain: remove the "robots noindex" line from every page, replace sample photos,
and add the Privacy Policy and Terms pages (the footer links are placeholders).
''')
total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
nfiles = sum(len(fs) for _, _, fs in os.walk(OUT))
print('total', total // 1024, 'KB in', nfiles, 'files')
