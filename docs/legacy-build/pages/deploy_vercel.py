# Vercel version of the site (user, 29 Oct: "lets connect this to vercel"). Starts from the Netlify build
# (/tmp/claude-0/deploy/sinelab-website, made by deploy2.py) and changes only what Vercel needs:
#  - forms: Netlify Forms don't exist on Vercel, so both enquiry forms post to FormSubmit (AJAX endpoint for
#    info@sinelabtechnologies.com; no account needed, the inbox confirms once via an activation email)
#  - cache/security headers move from _headers to vercel.json
import shutil, json, os
SRC = '/tmp/claude-0/deploy/sinelab-website/'; OUT = '/tmp/claude-0/deploy/sinelab-website-vercel/'
shutil.rmtree(OUT, ignore_errors=True); shutil.copytree(SRC, OUT)
os.remove(OUT + '_headers')
TO = 'https://formsubmit.co/ajax/info@sinelabtechnologies.com'
OLD_SEND = "fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(FORM)).toString() })"
NEW_SEND = ("fetch('" + TO + "', { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(FORM) })"
            ".then(r => r.json().catch(() => ({})).then(j => ({ ok: r.ok && String(j.success) !== 'false', status: r.status })))")
def rp(s, a, b, label):
    assert s.count(a) == 1, (label, s.count(a), a[:80]); return s.replace(a, b)
for page, fname, where in [('index.html', 'homepage-enquiry', 'homepage'), ('contact.html', 'enquiry', 'Contact page')]:
    s = open(OUT + page).read()
    s = rp(s, f'name="{fname}" method="post" data-netlify="true" netlify-honeypot="bot-field" novalidate>', f'name="{fname}" method="post" novalidate>', page)
    s = rp(s, f'<input type="hidden" name="form-name" value="{fname}">',
           f'<input type="hidden" name="_subject" value="New enquiry from the Sinelab website ({where})"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">', page)
    s = rp(s, '<input name="bot-field" tabindex="-1" autocomplete="off">', '<input name="_honey" tabindex="-1" autocomplete="off">', page)
    s = s.replace("form.querySelector('[name=\"bot-field\"]')", "form.querySelector('[name=\"_honey\"]')")
    s = rp(s, OLD_SEND, NEW_SEND, page)
    assert 'netlify' not in s.lower() and 'bot-field' not in s, page
    open(OUT + page, 'w').write(s)
CACHE = [{'key': 'Cache-Control', 'value': 'public, max-age=604800, stale-while-revalidate=86400'}]
json.dump({'headers': [{'source': '/assets/(.*)', 'headers': CACHE}, {'source': '/media/(.*)', 'headers': CACHE},
                       {'source': '/(.*)', 'headers': [{'key': 'X-Content-Type-Options', 'value': 'nosniff'},
                                                       {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'}]}]},
          open(OUT + 'vercel.json', 'w'), indent=2)
open(OUT + 'README.txt', 'w').write('''SINELAB TECHNOLOGIES WEBSITE (Vercel version)

Pages: index.html (home), about.html, solutions.html, projects.html, gallery.html, contact.html
assets/  images, fonts, animation libraries      media/  milestone films      vercel.json  caching + security headers

Vercel settings: Framework Preset "Other", no build command, output directory = the repository root.

Forms: the homepage form and the Contact page form send to info@sinelabtechnologies.com through FormSubmit
(formsubmit.co). The first enquiry triggers a one-time "Activate form" email to that inbox. Click Activate once;
after that every enquiry arrives as an email.

Before launch on the real domain: remove the "robots noindex" line from every page and add the Privacy Policy
and Terms pages (the footer links are placeholders).
''')
n = sum(len(fs) for _, _, fs in os.walk(OUT)); print('vercel build', n, 'files')
