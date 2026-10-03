from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'backend/config/template-presets.json';d=json.loads(p.read_text(encoding='utf-8'))
m={'elegant-luxury':['Jazz','Classic','Instrumental'],'garden-dream':['Acoustic','Folk'],'classic-vintage':['Jazz','Classic'],'blush':['Acoustic','Upbeat'],'celestial':['Ambient','Piano'],'editorial':['Classic','Jazz'],'ocean-vows':['Acoustic','Tropical'],'royal-heritage':['Orchestral','Classic'],'botanica':['Tropical','Acoustic'],'monochrome':['Piano','Jazz'],'neon-love':['Modern','Electronic Chill'],'timeless-romance':['Classic','Piano','Orchestral']}
for k,v in m.items():d[k]['mood']=v
g=['Floral masonry','Asymmetric editorial grid','Clean grid','Framed heritage gallery','Garden photo board','Vintage album','Night snap reel','Geometric gallery','Cinematic reel','Creative collage']
for k,v in zip(list(d)[:10],g):d[k]['gallery_style']=v
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8').replace('Ten visual templates','Twenty visual templates').replace('Experience tests cover 100 template/viewport combinations','Experience tests cover 200 template/viewport combinations')
s+='\n\n## Upgrade: 20-template collection\n\nRADINA now includes twenty developer-managed designs, a 50-track original demo music library, eleven marketplace categories, persistent favorites, and comparison of up to three templates. Existing customer data and payment flow remain unchanged. See [the upgrade guide](docs/TWENTY-TEMPLATES.md) for the new collection, setup commands, architecture, asset notes and tests.\n'
p.write_text(s,encoding='utf-8')
p=root/'frontend/public/ASSET-CREDITS.md';p.write_text('\n'.join(line for line in p.read_text(encoding='utf-8').splitlines() if 'photo-20.webp:' not in line)+'\n',encoding='utf-8')
