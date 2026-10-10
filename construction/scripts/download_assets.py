"""Download public media listed in the captured migration manifest."""
from pathlib import Path
import json,urllib.request,concurrent.futures
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'construction/reference/asset-manifest.json').read_text())
def fetch(item):
 path,url=item;target=ROOT/'dist'/path
 if target.exists() and target.stat().st_size:return path,'cached'
 target.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept-Encoding':'identity','Connection':'close'}),timeout=60) as response:target.write_bytes(response.read())
  return path,target.stat().st_size
 except Exception as error:return path,str(error)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,manifest.items()))
errors=[(p,r) for p,r in results if not isinstance(r,int) and r!='cached']
for result in errors:print(*result)
print(f'{len(results)-len(errors)}/{len(results)} assets available.')
if errors:raise SystemExit(1)
