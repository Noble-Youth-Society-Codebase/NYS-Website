"""Validate local references and preserved members using the standard library."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]
DIST=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=set();self.refs=[];self.members=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='article' and 'member' in a.get('class','').split():self.members+=1
  for key in ['src','href','poster']:
   if a.get(key):self.refs.append(a[key])
def paths(value):
 if isinstance(value,dict):
  for item in value.values():yield from paths(item)
 elif isinstance(value,list):
  for item in value:yield from paths(item)
 elif isinstance(value,str) and value.startswith('assets/'):yield value
pages={p.resolve():Page(p.read_text(encoding='utf-8')) for p in DIST.rglob('*.html')}
errors=[]
def check(ref,source):
 url=urlsplit(ref)
 if url.scheme or url.netloc:return
 target=(source.parent/unquote(url.path)).resolve() if url.path else source
 if not target.is_relative_to(DIST.resolve()):errors.append(f'Outside dist: {ref}');return
 if target.is_dir():target=target/'index.html'
 if not target.is_file():errors.append(f'{source.relative_to(ROOT)}: missing {ref}')
 elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:errors.append(f'Missing fragment: {ref}')
for path,page in pages.items():
 for ref in page.refs:check(ref,path)
for path in DIST.rglob('*.css'):
 for ref in re.findall(r"url\(['\"]?([^'\")]+)",path.read_text(encoding='utf-8')):check(ref,path.resolve())
data=json.loads((ROOT/'construction/content.json').read_text(encoding='utf-8'))
for ref in set(paths(data)):check(ref,DIST/'index.html')
if not (DIST/'index.html').is_file():errors.append('Missing homepage')
memberpath=(DIST/'our-members.html').resolve()
if memberpath not in pages or pages[memberpath].members!=len(data['members']):errors.append('Incorrect member count')
else:
 text=memberpath.read_text(encoding='utf-8')
 if Counter(re.findall(r'<h4 class="member-name">(.*?)</h4>',text))!=Counter(escape(m['name'],quote=True) for m in data['members']):errors.append('Incorrect member names')
if errors:print('\n'.join(errors),file=sys.stderr);raise SystemExit(1)
print(f'Passed: {len(pages)} HTML files, local links/fragments, CSS/content assets, and {len(data["members"])} profiles.')
