"""Build the portable website. Python standard library only."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,re,shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True);(OUT/'assets').mkdir(exist_ok=True)
for asset in (ROOT/'construction/assets').iterdir():
 if asset.is_file():shutil.copyfile(asset,OUT/'assets'/asset.name)
d=json.loads((ROOT/'construction/content.json').read_text(encoding='utf-8'))
NAV=[('index','HOME'),('past-events','PAST EVENTS'),('upcoming-events','UPCOMING EVENTS'),('our-members','OUR MEMBERS'),('join-us','JOIN US')]
def e(v):return escape(str(v),quote=True)
def para(text):return '<p>'+e(text).replace('\n','<br>')+'</p>'
def image(src,alt,cls='',lazy=True):return f'<img src="{e(src)}" alt="{e(alt)}" class="{cls}"'+(' loading="lazy"' if lazy else '')+' decoding="async">'
def page(slug,title,body):
 links=''.join(f'<a href="{s}.html"'+(' aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in NAV)
 html=f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Noble Youth Society</title><meta name="description" content="Youth-led volunteering and community service in Metro Vancouver since 2017.">
<link rel="icon" href="{d['logo']}"><link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="assets/styles.css">
{'<link rel="stylesheet" href="assets/members.css">' if slug=='our-members' else ''}
<script src="assets/data.js" defer></script><script src="assets/site.js" defer></script></head>
<body class="page-{slug}"><a class="skip-link" href="#main">Skip to Main Content</a>
<header class="site-header"><div class="brand-row"><a class="brand-logo" href="index.html" aria-label="Noble Youth Society home">{image(d['logo'],'Noble Youth Society logo',lazy=False)}</a><a class="brand-title" href="index.html">NOBLE YOUTH SOCIETY</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open navigation">☰</button></div><nav class="site-nav" id="site-nav" aria-label="Main navigation">{links}</nav></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="footer-brand">{image(d['footerLogo'],'Noble Youth Society logo')}<span>Noble Youth Society</span></div><a href="mailto:nobleyouthsociety@gmail.com">nobleyouthsociety@gmail.com</a><a href="https://www.instagram.com/nysnobleyouthsociety/" target="_blank" rel="noopener noreferrer">Instagram</a><p>©2022 by Noble Youth Society.</p></footer>
<button class="chat-toggle" aria-expanded="false" aria-controls="chat-panel">Let's Chat!</button><aside class="chat-panel" id="chat-panel" aria-label="Contact Noble Youth Society" hidden><div class="chat-heading">Noble Youth Society<button class="chat-close" aria-label="Close contact panel">×</button></div><p>Hi! We'd love to hear from you.</p><a class="button" href="mailto:nobleyouthsociety@gmail.com">Email us</a><a href="index.html#contact">Write a message</a></aside>
<dialog class="lightbox" id="lightbox" aria-label="Photo viewer"><button class="lightbox-close" aria-label="Close photo viewer">×</button><div class="lightbox-body"><button class="lightbox-prev" aria-label="Previous photo">‹</button><figure><img id="lightbox-image" alt=""><figcaption id="lightbox-caption"></figcaption></figure><button class="lightbox-next" aria-label="Next photo">›</button></div></dialog>
</body></html>"""
 (OUT/f'{slug}.html').write_text(html,encoding='utf-8')
fields=''.join(f'<label><span class="sr-only">{label}</span><input name="{name}" type="{kind}" placeholder="{label}" maxlength="250"'+(' required' if required else '')+'></label>' for name,label,kind,required in [('name','Name','text',True),('email','Email','email',True),('phone','Phone','tel',False),('address','Address','text',False),('subject','Subject','text',False)])
home=f"""<section class="welcome-section"><div class="welcome-inner">{image(d['hero'],'NYS volunteers at a community fundraiser','welcome-photo',False)}<div class="welcome-card"><h1>Welcome</h1>{para(d['welcome'])}<a class="button" href="#contact">Get in Touch</a></div></div></section>
<section class="home-gallery" aria-label="Slide show gallery"><div class="slideshow"><button class="slide-image" aria-label="Enlarge current photo">{image(d['slides'][0],'Noble Youth Society photo 1 of 24',lazy=False)}</button><button class="slide-prev" aria-label="Previous">‹</button><button class="slide-next" aria-label="Next">›</button><span class="slide-counter" aria-live="polite">1/24</span></div></section>
<section class="contact-section" id="contact"><h2>CONTACT US</h2><form id="contact-form"><div class="form-grid">{fields}<label class="full"><span class="sr-only">Message</span><textarea name="message" placeholder="Type your message here..." rows="5" maxlength="5000" required></textarea></label></div><button class="button submit" type="submit">Submit</button><p class="form-note">Send your message with your email app.</p></form></section>
<dialog class="message-dialog" id="message-dialog" aria-labelledby="message-title"><button class="message-close" aria-label="Close message preview">×</button><h2 id="message-title">Your message is ready</h2><p>Open your email app to send it to Noble Youth Society.</p><pre id="message-preview"></pre><div class="message-actions"><a id="email-draft" class="button" href="mailto:nobleyouthsociety@gmail.com">Open email app</a><button type="button" id="copy-message" class="button button-outline">Copy message</button></div><p id="copy-status" role="status"></p></dialog>"""
page('index','HOME',home)
archive=f'<section class="events-hero">{image(d["eventHero"],"NYS Halloween",lazy=False)}<h1>Empowering<br>Youth Since Day 1</h1></section><div class="event-archive">'
for number,event in enumerate(d['events']):
 if 'year' in event:archive+=f'<div class="year-marker"><h2>{e(event["year"])}</h2></div>';continue
 photos=''.join(f'<button class="event-image" data-photo="{e(src)}" data-caption="{e(event["title"])}" aria-label="Enlarge {e(event["title"])}">{image(src,event["title"])}</button>' for src in event['images'])
 actions=''
 for action in event['actions']:
  if 'url' in action:actions+=f'<a class="button" href="{e(action["url"])}" target="_blank" rel="noopener noreferrer">{e(action["label"])}</a>'
  else:actions+=f'<button class="button" data-photo="{e(action["image"])}" data-caption="{e(event["title"])}">{e(action["label"])}</button>'
 archive+=f'<article class="event-row '+('image-first ' if number%2 else '')+('text-event' if not photos else '')+f'"><div class="event-copy"><h3 class="event-title">{e(event["title"])}</h3><div class="event-description">'+''.join(para(p) for p in event['paragraphs'])+f'</div><div class="event-actions">{actions}</div></div>'+ (f'<div class="event-media">{photos}</div>' if photos else '')+'</article>'
page('past-events','PAST EVENTS',archive+'</div>')
def member_card(m):return f'<article class="member">{image(m["image"],m["name"],"member-photo")}<div class="member-copy"><p class="member-role">{e(m["role"])}</p><h4 class="member-name">{e(m["name"])}</h4>'+''.join(para(p) for p in m['paragraphs'])+'</div></article>'
def rank(m):
 role=m['role'].casefold()
 if role.startswith(('co-president','president')):return 0
 if 'vice president' in role or role.startswith('vp '):return 1
 if 'director' in role:return 2
 return 3
current=[m for m in d['members'] if not m['role'].casefold().startswith('past ')]
past=[m for m in d['members'] if m['role'].casefold().startswith('past ')]
team='<section class="team-section"><div class="team-intro"><h1>Our Team</h1><p class="team-subtitle">Empowering Youth Since Day One</p><p>Organized and led by high-school students, Noble Youth Society is a non-profit organization based in Metro Vancouver, Canada.</p><nav class="team-section-nav" aria-label="Team sections"><a href="#current-leadership">Current leadership ↓</a><a href="#past-leadership">Past leadership ↓</a></nav></div>'
team+=f'<section class="leadership-section" id="current-leadership" aria-labelledby="current-heading"><header class="leadership-heading"><h2 id="current-heading">Current leadership</h2><span>{len(current)} team members</span></header>'
for r,label in enumerate(['Co-Presidents','Vice Presidents','Directors','Officers & Assistants']):
 group=[m for m in current if rank(m)==r]
 if group:team+=f'<section class="leadership-group" aria-labelledby="tier-{r}"><h3 class="tier-heading" id="tier-{r}"><span class="tier-number" aria-hidden="true">{r+1:02}</span>{e(label)}</h3><div class="members">'+''.join(member_card(m) for m in group)+'</div></section>'
team+='</section>'
team+=f'<section class="leadership-section past-leadership" id="past-leadership" aria-labelledby="past-heading"><header class="leadership-heading"><h2 id="past-heading">Past leadership</h2><span>{len(past)} team members</span></header>'
def term(m):
 match=re.search(r'\b20\d{2}\b',m['role']);return match.group() if match else 'Previous leadership'
for year in sorted({term(m) for m in past},reverse=True):
 group=[m for m in past if term(m)==year];identifier=year.replace(' ','-')
 team+=f'<section class="leadership-group" aria-labelledby="term-{identifier}"><h3 class="tier-heading" id="term-{identifier}">{e(year)}</h3><div class="members">'+''.join(member_card(m) for m in group)+'</div></section>'
page('our-members','OUR MEMBERS',team+'</section></section>')
page('upcoming-events','UPCOMING EVENTS','<section class="coming-soon"><h1>(More) Coming Soon<br>Stay Tuned<br>: )</h1></section>')
page('join-us','JOIN US',f'<section class="join-section"><video autoplay muted loop playsinline poster="{d["joinPoster"]}" aria-hidden="true"><source src="{d["joinVideo"]}" type="video/mp4"></video><a class="enrollment-link" href="{e(d["enrollmentUrl"])}" target="_blank" rel="noopener noreferrer">NYS Enrollment Form <span aria-hidden="true">›</span></a></section>')
page('search','Search Results','<section class="utility-section"><h1>Search Results</h1><form id="search-form" role="search"><label for="search-input">Search this site</label><div class="search-control"><input id="search-input" type="search" name="q" placeholder="Search this site"><button class="button">Search</button></div></form><p id="search-summary" aria-live="polite"></p><div id="search-results"></div></section>')
page('schedule','Schedule','<section class="utility-section empty-schedule"><h1>No Schedule to display at the moment</h1></section>')
page('event-details-registration','Event Details & Registration','<section class="utility-section sample-event"><h1>MY EVENT</h1>'+''.join(para(p) for p in d['sampleEventParagraphs'])+'<a class="button" href="https://nysvancouver.wixsite.com/noble-youth-society/event-details-registration" target="_blank" rel="noopener noreferrer">RSVP on original website</a></section>')
class MainTextParser(HTMLParser):
 def __init__(self):super().__init__();self.in_main=False;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag=='main':self.in_main=True
 def handle_endtag(self,tag):
  if tag=='main':self.in_main=False
 def handle_data(self,text):
  if self.in_main and text.strip():self.parts.append(text.strip())
search=[]
for slug,title in NAV:
 parser=MainTextParser();parser.feed((OUT/f'{slug}.html').read_text(encoding='utf-8'));search.append({'title':title+' | Noble Youth Society','url':slug+'.html','text':' '.join(parser.parts)})
(OUT/'assets/data.js').write_text('window.NYS_DATA = '+json.dumps({'slides':d['slides'],'search':search},ensure_ascii=False)+';\n',encoding='utf-8')
aliases={'blank':'index','blank-1':'past-events','blank-2':'our-members','past-events':'past-events','upcoming-events':'upcoming-events','our-members':'our-members','join-us':'join-us','search':'search','schedule':'schedule','event-details-registration':'event-details-registration'}
for alias,slug in aliases.items():
 folder=OUT/alias;folder.mkdir(exist_ok=True);(folder/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../{slug}.html"><title>Noble Youth Society</title></head><body><a href="../{slug}.html">Continue to Noble Youth Society</a></body></html>',encoding='utf-8')
print('Built eight pages and ten route aliases.')
