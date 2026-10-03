"""Optional development tool: licensed stock photos and original synthesized demos."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, subprocess, json, math, wave, array
root=Path(__file__).resolve().parents[1]
ids=[16496378,15878571,18858563,17444441,9061879,5729059,31715498,10792715,35035139,10258989]
def download(pair):
 n,identifier=pair;dest=root/f'frontend/public/images/demos/photo-{n+21}.webp'
 if dest.exists():return
 tmp=root/f'.local-tools/expanded-{n}.jpg'
 req=urllib.request.Request(f'https://images.pexels.com/photos/{identifier}/pexels-photo-{identifier}.jpeg?auto=compress&cs=tinysrgb&w=1000',headers={'User-Agent':'Mozilla/5.0'})
 tmp.write_bytes(urllib.request.urlopen(req,timeout=40).read())
 subprocess.run(['php',str(root/'scripts/convert-demo-image.php'),str(tmp),str(dest)],check=True,stdout=subprocess.DEVNULL)
 tmp.unlink();print('Photo',n+21,'ready',flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,enumerate(ids)))
music=root/'frontend/public/music/library'
catalog=json.loads((music/'catalog.json').read_text(encoding='utf-8'))[:10]
categories=['Ambient','Jazz','Acoustic','Orchestral','Piano','Tropical','Classic','Instrumental','Electronic Chill','Classic','Romantic','Piano','Acoustic','Classic','Islamic','Traditional','Cinematic','Modern','Upbeat','Folk']
titles=['Moonlight Promise','The Wedding Issue','Saltwater Serenade','A Royal Prelude','Pressed Petals','Palm Breeze','Silver Portraits','Blossom Reverie','City Afterglow','Maison Romance','Ivory Morning','A Gentle Yes','Forever Shore','The Quiet Waltz','Peaceful Steps','Golden Courtyard','Our First Scene','Soft Skyline','Paper Hearts','Across the Garden']
for number in range(11,51):
 i=number-11;category=categories[i%20];title=titles[i%20]+(' II' if i>=20 else '')
 dest=music/f'track-{number}.mp3';duration=18
 if not dest.exists():
  rate=22050; samples=[0.0]*(rate*duration);tempo=.38+(i%9)*.055
  chords=[[48,52,55],[45,48,52],[41,45,48],[43,47,50]] if i%2==0 else [[50,53,57],[46,50,53],[48,52,55],[45,50,53]]
  for beat in range(int(duration/tempo)):
   start=beat*tempo;pitch=chords[(beat//5+i)%4][beat%3]+12+(i%12)-5;freq=440*2**((pitch-69)/12)
   for j in range(min(int(rate*1.65),len(samples)-int(start*rate))):
    t=j/rate;env=(1-math.exp(-t*30))*math.exp(-t*(2.2+(i%3)*.3))*(1-t/1.65)
    samples[int(start*rate)+j]+=.16*env*(math.sin(2*math.pi*freq*t)+(.12+(i%4)*.04)*math.sin(4*math.pi*freq*t))
  pcm=array.array('h',(int(max(-1,min(1,v))*24000*min(1,j/rate,(duration-j/rate)/2)) for j,v in enumerate(samples)))
  tmp=music/'expanded-temporary.wav'
  with wave.open(str(tmp),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(pcm.tobytes())
  subprocess.run([str(root/'.local-tools/ffmpeg.exe'),'-y','-i',str(tmp),'-codec:a','libmp3lame','-b:a','80k',str(dest)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  tmp.unlink();print('Music',number,'ready',flush=True)
 catalog.append({'title':title,'artist':'Radina Originals','category':category,'file_url':f'/music/library/track-{number}.mp3','duration':duration,'is_active':True,'is_featured':False})
(music/'catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
credits=root/'frontend/public/ASSET-CREDITS.md'
s=credits.read_text(encoding='utf-8')
if 'Expanded collection 11–20' not in s:
 s+='\n## Expanded collection 11–20\n\nFictional demo identities. Additional Pexels stock photography; no endorsement implied.\n'+''.join(f'- photo-{i+21}.webp: https://www.pexels.com/photo/{identifier}/\n' for i,identifier in enumerate(ids))+'\nTracks 11–50 are original synthesized demonstration instrumentals generated for this project, not third-party recordings. All 50 tracks are short demo cues; upload licensed full-length recordings for production.\n'
 credits.write_text(s,encoding='utf-8')
