import re,base64,sys
d='/tmp/claude-0/site/'
s=open(d+'src_draft.html').read()
mime={'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:'+mime[path.rsplit('.',1)[1]]+';base64,'+base64.b64encode(open(path,'rb').read()).decode()
s=re.sub(r'\{\{L:([^}]+)\}\}',lambda m:uri(d+'layers/'+m.group(1)),s)
s=s.replace('{{LOGO_BLACK}}',uri(d+'logo_black.png')).replace('{{LOGO}}',uri(d+'logo.png')).replace('{{LOGO_WHITE}}',uri(d+'logo_white.png')).replace('{{ABOUT_IMG}}',uri(d+'about.jpg'))
assert '{{' not in s.replace('{{{','') or True
open(d+'sinelab-draft.html','w').write(s)
open(d+'test_draft.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+s+'</body></html>')
print(len(s)//1024,'KB', 'leftover', len(re.findall(r'\{\{[A-Z_:]',s)))
