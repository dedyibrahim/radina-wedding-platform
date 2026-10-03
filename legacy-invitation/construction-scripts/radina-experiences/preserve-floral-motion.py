from pathlib import Path
root=Path(__file__).resolve().parents[1]/'frontend/src/templates'
for name in ['DesignCouple','DesignStory','DesignEvent','DesignClosing']:
 p=root/'shared'/f'{name}.vue';s=p.read_text(encoding='utf-8');s=s.replace('<script setup>','<script setup>\nimport FlowerMotion from "../RomanticFloral/components/FlowerMotion.vue"',1)
 start=s.index('<section');end=s.index('>',start)+1;s=s[:end]+"\n<FlowerMotion v-if=\"['amore','garden','daydream'].includes(design)\" />"+s[end:];p.write_text(s,encoding='utf-8')
for folder in ['RomanticFloral','GardenDream','Blush']:
 for name in ['Opening','Hero']:
  p=root/folder/f'{name}.vue';s=p.read_text(encoding='utf-8');s=s.replace('<script setup>','<script setup>\nimport FlowerMotion from "../RomanticFloral/components/FlowerMotion.vue"',1);start=s.index('<section');end=s.index('>',start)+1;s=s[:end]+'\n<FlowerMotion />'+s[end:];p.write_text(s,encoding='utf-8')
styles={
 'ElegantLuxury': '.design-noir .reveal-ready{transform:none;transition:opacity 1.4s ease}.design-noir .reveal-ready.is-visible{transform:none}@media(min-width:768px){.design-noir .couple-layout{grid-template-columns:1fr}}',
 'MinimalistWhite': '.design-pure .reveal-ready,.design-pure .reveal-ready.is-visible{transform:none}',
 'MidnightRomance': '.design-dark .reveal-ready{filter:blur(7px);transform:scale(.98);transition:opacity 1s ease,filter 1s ease,transform 1s ease}.design-dark .reveal-ready.is-visible{filter:blur(0);transform:scale(1)}@media(min-width:768px){.design-dark .couple-layout{grid-template-columns:1fr 1fr;gap:0}}',
 'Sakinah': '.design-sakinah .reveal-ready,.design-sakinah .reveal-ready.is-visible{transform:none;transition:opacity .65s ease}',
 'EternalStory': '.hero-cinema .hero-full-photo{animation:cinema-slow-zoom 28s linear infinite alternate}@keyframes cinema-slow-zoom{to{transform:scale(1.08)}}',
 'Blush': '.design-daydream .hero-copy h1,.design-daydream .section-heading h2{font-family:"DM Sans",sans-serif;font-weight:400;letter-spacing:-.04em}.design-daydream .hero-copy h1{font-size:clamp(2.3rem,var(--name-scale,14vw),4.5rem)}',
 'ClassicVintage': '.design-letters .invitation-letter h1{font-style:italic}',
}
for folder,style in styles.items():
 p=root/folder/'presentation.css';p.write_text(p.read_text(encoding='utf-8')+'\n'+style+'\n',encoding='utf-8')
