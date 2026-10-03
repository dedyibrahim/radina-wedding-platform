from pathlib import Path
root=Path(__file__).resolve().parents[1]
for p in (root/'frontend/src/templates').glob('*/Hero.vue'):
 s=p.read_text(encoding='utf-8').replace('aria-label="Lanjutkan cerita"','aria-label="Gulir ke cerita kami"')
 s=s.replace('<div class="hero-copy">','<div class="hero-copy"><p v-if="wedding.sections.home?.heading" class="hero-kicker">{{ wedding.sections.home.heading }}</p>')
 s=s.replace('<header class="pure-hero-header">','<header class="pure-hero-header"><small>{{ wedding.sections.home?.heading }}</small>')
 p.write_text(s,encoding='utf-8')
for p in (root/'frontend/src/templates').glob('*/Opening.vue'):
 s=p.read_text(encoding='utf-8').replace('wedding.sections.home?.content || wedding.openingText','wedding.openingText');p.write_text(s,encoding='utf-8')
p=root/'frontend/src/templates/ClassicVintage/presentation.css';s=p.read_text(encoding='utf-8').replace('.hero-letters .hero-scroll{display:none}', '.hero-letters .hero-scroll{display:block}.hero-letters{padding-bottom:90px}');p.write_text(s,encoding='utf-8')
p=root/'scripts/platform-test.mjs';s=p.read_text(encoding='utf-8').replace("name: 'Romantic Floral'","name: 'Amore Bloom'").replace("name: 'Elegant Luxury'","name: 'Noir Élégance'");p.write_text(s,encoding='utf-8')
p=root/'scripts/radina-test.mjs';s=p.read_text(encoding='utf-8').replace("const base = 'http://localhost:5173'", "const base = process.env.TEST_URL || 'http://localhost:5173'");p.write_text(s,encoding='utf-8')
for filename,section in [('VideoSection.vue','video'),('LocationSection.vue','location'),('LiveStreaming.vue','livestream')]:
 p=root/'frontend/src/templates/RomanticFloral/components'/filename;s=p.read_text(encoding='utf-8');s=s.replace('<section class=',f'<section id="{section}" class=');p.write_text(s,encoding='utf-8')
