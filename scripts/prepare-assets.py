"""Download demo photographs and produce an original instrumental + silent film."""
from pathlib import Path
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import math, wave, struct, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
PHOTOS = {
 'cover': ('1519741497674-611481863552', 1000),
 'hero': ('1591604466107-ec97de577aff', 850),
 'bride': ('1524504388940-b1c1722653e1', 450),
 'groom': ('1500648767791-00dcc994a43e', 450),
 'closing': ('1511285560929-80b456fea0bc', 850),
 'moment-1': ('1591604466107-ec97de577aff', 650),
 'moment-2': ('1519741497674-611481863552', 650),
 'moment-3': ('1523438885200-e635ba2c371e', 650),
 'moment-4': ('1511285560929-80b456fea0bc', 650),
 'moment-5': ('1532712938310-34cb3982ef74', 650),
 'moment-6': ('1511795409834-ef04bbd61622', 650),
}
for name, (photo, width) in list(PHOTOS.items()):
 if name in ['cover', 'hero'] or name.startswith('moment-'):
  PHOTOS[name + '-small'] = (photo, 600 if name == 'cover' else 400 if name == 'hero' else 320)
def download(item):
 name, (photo, width) = item
 target = ROOT / 'public' / 'images' / (name + '.webp')
 target.parent.mkdir(parents=True, exist_ok=True)
 url = f'https://images.unsplash.com/photo-{photo}?auto=format&fit=crop&w={width}&q=80&fm=webp'
 with urllib.request.urlopen(url, timeout=60) as response:
  target.write_bytes(response.read())
 print(name, target.stat().st_size)
with ThreadPoolExecutor(max_workers=5) as pool:
 list(pool.map(download, PHOTOS.items()))
credits = '# Demo assets\n\nPhotographs are from Unsplash and are illustrative stock photographs, not actual portraits of Alya and Rizky. Replace before publishing.\n\n'
for name, (photo, _) in PHOTOS.items():
 credits += f'- {name}: https://images.unsplash.com/photo-{photo}\n'
credits += '\nMusic: original synthesized instrumental generated for this project, no third-party recording. Video: silent slideshow of the credited photographs.\n'
(ROOT / 'public' / 'ASSET-CREDITS.md').write_text(credits, encoding='utf-8')
sys.path.insert(0, str(ROOT / 'scripts' / 'vendor'))
import imageio_ffmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
music_dir = ROOT / 'public' / 'music'
music_dir.mkdir(exist_ok=True)
wav_path = ROOT / 'scripts' / 'instrumental-temp.wav'
rate, duration = 22050, 48
progression = [[48,52,55,59], [45,48,52,55], [41,45,48,52], [43,47,50,55]]
notes = []
for bar in range(16):
 chord = progression[bar % 4]
 for beat in range(6):
  notes.append((bar*3+beat*.5, chord[beat%4]+12, 1.8, .14))
 notes.append((bar*3, chord[0], 2.9, .14))
 notes.append((bar*3+1.5, chord[2]+24, 1.4, .055))
def hz(midi): return 440 * 2 ** ((midi-69)/12)
with wave.open(str(wav_path), 'wb') as output:
 output.setnchannels(1); output.setsampwidth(2); output.setframerate(rate)
 frames = bytearray()
 for i in range(rate*duration):
  t=i/rate; value=0
  for start, pitch, length, amplitude in notes:
   x=t-start
   if 0<=x<length:
    freq=hz(pitch)
    envelope=(1-math.exp(-x*30))*math.exp(-x*2.2)*(1-x/length)
    value+=amplitude*envelope*(math.sin(2*math.pi*freq*x)+.22*math.sin(2*math.pi*freq*2*x)+.06*math.sin(2*math.pi*freq*3*x))
  value*=min(1,t/2,(duration-t)/3)
  frames.extend(struct.pack('<h',int(max(-1,min(1,value))*28000)))
 output.writeframes(frames)
subprocess.run([ffmpeg,'-y','-i',str(wav_path),'-codec:a','libmp3lame','-b:a','96k',str(music_dir/'wedding-song.mp3')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
wav_path.unlink()
video_dir=ROOT/'public'/'video'; video_dir.mkdir(exist_ok=True)
subprocess.run([ffmpeg,'-y','-loop','1','-t','4','-i',str(ROOT/'public'/'images'/'moment-1.webp'),'-loop','1','-t','4','-i',str(ROOT/'public'/'images'/'moment-4.webp'),'-loop','1','-t','4','-i',str(ROOT/'public'/'images'/'moment-6.webp'),'-filter_complex','[0:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,setsar=1[v0];[1:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,setsar=1[v1];[2:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,setsar=1[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]','-map','[v]','-r','24','-c:v','libx264','-pix_fmt','yuv420p','-crf','28','-movflags','+faststart',str(video_dir/'our-story.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('Original music and demo film ready.')
