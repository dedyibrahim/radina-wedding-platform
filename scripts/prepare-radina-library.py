"""Development asset preparation; not part of runtime. Stock demo photos and original generated music."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, io, json, math, wave, struct, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'.local-tools/python-libs'))
root=Path(__file__).resolve().parents[1]
out=root/'frontend/public/images/demos';out.mkdir(parents=True,exist_ok=True)
ids=[265722,1024993,1444442,1043902,169198,2959192,931796,1468379,313707,2253870,1488318,291759,1589216,1779414,3014859,1779491,1616113,1702373,5804909,5904782]
def photo(item):
 i,identifier=item;target=out/f'photo-{i+1}.webp'
 if target.exists(): return
 url=f'https://images.pexels.com/photos/{identifier}/pexels-photo-{identifier}.jpeg?auto=compress&cs=tinysrgb&w=1000'
 try:
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(request,timeout=35) as response: raw=response.read()
  temporary=root/'.local-tools'/f'demo-photo-{i+1}.jpg';temporary.write_bytes(raw)
  subprocess.run(['php',str(root/'scripts/convert-demo-image.php'),str(temporary),str(target)],check=True,stdout=subprocess.DEVNULL)
  temporary.unlink()
  print('photo',i+1,'ready',flush=True)
 except Exception as error: print('photo',i+1,'failed',type(error).__name__,flush=True)
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(photo,enumerate(ids)))
music=root/'frontend/public/music/library';music.mkdir(parents=True,exist_ok=True)
ffmpeg=root/'.local-tools/ffmpeg.exe'
catalog=[('Petals at Dawn','Romantic',0,0.55),('Quiet Promises','Piano',2,0.65),('Golden Hour','Acoustic',-2,0.45),('A Timeless Letter','Classic',-5,0.7),('Under the Stars','Cinematic',-7,0.8),('A Peaceful Journey','Islamic',5,0.72),('Homeward','Traditional',7,0.58),('Little Daydream','Upbeat',4,0.36),('Still Together','Instrumental',-3,0.6),('Midnight Lights','Modern',1,0.48)]
for n,(title,category,transpose,tempo) in enumerate(catalog):
 target=music/f'track-{n+1}.mp3'
 if target.exists():continue
 rate=22050;duration=24;frames=bytearray();notes=[]
 progression=[[48,52,55],[45,48,52],[41,45,48],[43,47,50]]
 for beat in range(int(duration/tempo)):
  chord=progression[(beat//6)%4];notes.append((beat*tempo,chord[beat%3]+12+transpose,1.8,.18))
 with wave.open(str(music/'temporary.wav'),'wb') as output:
  output.setnchannels(1);output.setsampwidth(2);output.setframerate(rate)
  for sample in range(rate*duration):
   t=sample/rate;value=0
   for start,pitch,length,amp in notes:
    x=t-start
    if 0<=x<length:
     frequency=440*2**((pitch-69)/12);envelope=(1-math.exp(-x*35))*math.exp(-x*2)*(1-x/length)
     value+=amp*envelope*(math.sin(2*math.pi*frequency*x)+.17*math.sin(4*math.pi*frequency*x))
   value*=max(0,min(1,t/1.5,(duration-t)/2));frames.extend(struct.pack('<h',int(max(-1,min(1,value))*26000)))
  output.writeframes(frames)
 subprocess.run([str(ffmpeg),'-y','-i',str(music/'temporary.wav'),'-codec:a','libmp3lame','-b:a','96k',str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 print('music',n+1,'ready',flush=True)
if (music/'temporary.wav').exists():(music/'temporary.wav').unlink()
(music/'catalog.json').write_text(json.dumps([{'title':t,'category':c,'artist':'Radina Originals','file_url':f'/music/library/track-{i+1}.mp3','duration':24,'is_active':True,'is_featured':i<3} for i,(t,c,_,_) in enumerate(catalog)],indent=2),encoding='utf-8')
credits=root/'frontend/public/ASSET-CREDITS.md'
s=credits.read_text(encoding='utf-8')
if 'Radina experience demos' not in s:
 s+='\n## Radina experience demos\n\nFictional couples; stock imagery does not imply endorsement. Pexels license: https://www.pexels.com/license/\n\n'+''.join(f'- photo-{i+1}.webp: https://www.pexels.com/photo/{identifier}/\n' for i,identifier in enumerate(ids))+'\nMusic Library: ten original synthesized demonstration instrumentals by Radina Originals, generated for this project. No third-party song recordings. Titles are fictional original works.\n'
 credits.write_text(s,encoding='utf-8')
