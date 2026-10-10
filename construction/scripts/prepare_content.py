"""Optional extraction from captured public Wix HTML."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
ROOT=Path(__file__).resolve().parents[2]
REF=ROOT/'construction/reference'
manifest={}
def source(name):return BeautifulSoup((REF/(name+'.html')).read_text(encoding='utf-8'),'html.parser')
def clean(text):return text.replace('\u200b','').strip()
def paragraphs(el):return [clean(p.get_text('\n',strip=True)) for p in el.find_all('p') if clean(p.get_text('\n',strip=True))]
def media(url):
 match=re.search(r'(?:https://static.wixstatic.com/media/)?([^/]+\.(?:jpg|jpeg|png|webp|gif))',url or '',re.I)
 if not match:return url or ''
 name=match.group(1);path='assets/images/'+name
 manifest[path]='https://static.wixstatic.com/media/'+name+'/v1/fit/w_1600,h_1600,q_90/'+name
 return path
home=source('home')
data={'source':'https://nysvancouver.wixsite.com/noble-youth-society'}
data['logo']=media(home.find(id='SITE_HEADER').find('img')['src'])
data['footerLogo']=media(home.find(id='SITE_FOOTER').find('img')['src'])
data['hero']=media(home.find(id='comp-ldmo04y6').find('img')['src'])
data['welcome']=clean(home.find(id='comp-ldmo04zn1').get_text(' ',strip=True))
data['slides']=[]
for item in home.find(attrs={'data-testid':'slide-show-gallery'}).find_all(attrs={'data-testid':'gallery-item-ghost'}):
 image=item.find(attrs={'data-image-info':True})
 if image:data['slides'].append(media(json.loads(image['data-image-info'])['imageData']['uri']))
if (REF/'slides.json').exists():data['slides']=[media(uri) for uri in json.loads((REF/'slides.json').read_text())]
assert len(data['slides'])==24,len(data['slides'])
past=source('past-events')
data['eventHero']=media(past.find(id='comp-l7g7y3nr').find('img')['src'])
data['events']=[]
for section in past.find('main').find_all('section'):
 if section.find_parent('section') or section.get('id')=='comp-l7g7y3nr':continue
 rich=section.find_all(attrs={'data-testid':'richTextElement'})
 if not rich:continue
 if len(rich)==1:data['events'].append({'year':clean(rich[0].get_text(' ',strip=True))});continue
 title=next((x for x in rich if x.find(['h1','h2','h3'])),min(rich,key=lambda x:len(x.get_text())))
 body=[p for x in rich if x!=title and not re.fullmatch(r'20\d{2}',x.get_text(strip=True)) for p in paragraphs(x)]
 images=[media(x.get('src')) for x in section.find_all('img')]
 actions=[{'label':a.get_text(' ',strip=True),'url':a['href']} for a in section.find_all('a',href=True)]
 if any(b.get_text(' ',strip=True)=='See Photos' or b.get('aria-label')=='See Photos' for b in section.find_all('button')) and images:actions.insert(0,{'label':'See Photos','image':images[0]})
 data['events'].append({'title':clean(title.get_text(' ',strip=True)),'paragraphs':body,'images':images,'actions':actions})
 for x in rich:
  if x!=title and re.fullmatch(r'20\d{2}',x.get_text(strip=True)):data['events'].append({'year':x.get_text(strip=True)})
team=source('our-members')
data['members']=[]
for role_node in team.find_all(id=re.compile(r'^comp-ldmqdvqo3__')):
 suffix=role_node['id'].split('__',1)[1]
 body=team.find(id='comp-ldmqdvqp4__'+suffix)
 photo=team.find(id='comp-ldmqdvqi__'+suffix).find('img')
 parts=paragraphs(body)
 if '\n' in parts[0]:
  name,remainder=parts[0].split('\n',1);parts=[name]+([remainder.strip()] if remainder.strip() else [])+parts[1:]
 data['members'].append({'name':parts[0],'role':clean(role_node.get_text(' ',strip=True)),'paragraphs':parts[1:],'image':media(photo['src'])})
join=source('join-us')
data['enrollmentUrl']=join.find('a',attrs={'aria-label':'NYS Enrollment Form'})['href']
data['joinPoster']=media(join.find(id='comp-le9oqcnp').find('img')['src'])
data['joinVideo']='assets/video/enrollment-background.mp4'
manifest[data['joinVideo']]='https://video.wixstatic.com/video/11062b_77378fc0da68439ebd8fd24a2f51e50c/720p/mp4/file.mp4'
data['sampleEventParagraphs']=list(dict.fromkeys(paragraphs(source('event-details-registration').find('main'))))
faces=[]
for style in home.find_all('style'):
 for face in re.findall(r'@font-face\s*\{[^}]+\}',style.get_text()):
  if any(name in face.lower() for name in ["'syne'","'questrial'","'oswald'"]) and ('U+0000-00FF' in face or 'unicode-range' not in face):faces.append(face)
css='\n'.join(dict.fromkeys(faces))
for url in re.findall(r"url\(['\"]?([^'\")]+)",css):
 name=url.rsplit('/',1)[-1];manifest['assets/fonts/'+name]='https:'+url if url.startswith('//') else url;css=css.replace(url,'fonts/'+name)
(ROOT/'construction/assets/fonts.css').write_text(css,encoding='utf-8')
(ROOT/'construction/content.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(REF/'asset-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
assert len(data['members'])==16
print(f'Extracted {len(data["members"])} profiles, {sum("title" in e for e in data["events"])} events, {len(data["slides"])} slides and {len(manifest)} assets.')
