from pathlib import Path
import urllib.request,subprocess
root=Path(__file__).resolve().parents[1]
for n,identifier in [(29,35035139),(30,10258989)]:
 req=urllib.request.Request(f'https://images.pexels.com/photos/{identifier}/pexels-photo-{identifier}.jpeg?auto=compress&cs=tinysrgb&w=1000',headers={'User-Agent':'Mozilla/5.0'})
 tmp=root/f'.local-tools/curated-{n}.jpg';tmp.write_bytes(urllib.request.urlopen(req,timeout=35).read())
 subprocess.run(['php',str(root/'scripts/convert-demo-image.php'),str(tmp),str(root/f'frontend/public/images/demos/photo-{n}.webp')],check=True,stdout=subprocess.DEVNULL)
 tmp.unlink()
p=root/'frontend/public/ASSET-CREDITS.md'
s=p.read_text(encoding='utf-8').replace('photo-29.webp: https://www.pexels.com/photo/20040304/','photo-29.webp: https://www.pexels.com/photo/35035139/').replace('photo-30.webp: https://www.pexels.com/photo/6607990/','photo-30.webp: https://www.pexels.com/photo/10258989/')
p.write_text(s,encoding='utf-8')
p=root/'scripts/prepare-expanded-library.py';p.write_text(p.read_text(encoding='utf-8').replace('20040304,6607990','35035139,10258989'),encoding='utf-8')
