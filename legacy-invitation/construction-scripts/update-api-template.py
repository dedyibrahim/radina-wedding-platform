from pathlib import Path
root=Path(__file__).resolve().parents[1]/'frontend'/'src'
components=root/'templates'/'RomanticFloral'/'components'
for path in components.glob('*.vue'):
    s=path.read_text(encoding='utf-8')
    s=s.replace('<span class="monogram">A<span>&</span>R</span>','<span class="monogram">{{ Array.from(wedding.bride.shortName)[0] }}<span>&</span>{{ Array.from(wedding.groom.shortName)[0] }}</span>')
    s=s.replace('<span class="small-monogram">A & R</span>','<span class="small-monogram">{{ Array.from(wedding.bride.shortName)[0] }} & {{ Array.from(wedding.groom.shortName)[0] }}</span>')
    s=s.replace('alt="Alya dan Rizky merayakan cinta mereka"', ':alt="`${wedding.bride.shortName} dan ${wedding.groom.shortName}`"')
    s=s.replace(':src="wedding.cover"','v-if="wedding.cover" :src="wedding.cover"').replace(':src="wedding.hero"','v-if="wedding.hero" :src="wedding.hero"').replace(':src="person.photo"','v-if="person.photo" :src="person.photo"').replace(':src="wedding.closing"','v-if="wedding.closing" :src="wedding.closing"')
    s=s.replace('subtitle="Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan kami."', ':subtitle="wedding.openingText"')
    s=s.replace('Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.', '{{ wedding.closingText }}')
    s=s.replace('<a :href="`https://www.instagram.com/${person.instagram}/`"','<a v-if="person.instagram" :href="`https://www.instagram.com/${person.instagram}/`"')
    s=s.replace('@click="downloadCalendar"','@click="downloadCalendar(wedding)"')
    s=s.replace('<p class="sample-note">Rekening dan alamat contoh — bukan untuk transaksi.</p>','')
    s=s.replace('<p class="sample-note">Alamat contoh. Konfirmasikan dengan pasangan sebelum mengirim.</p>','')
    s=s.replace('<p class="sample-note">Lokasi contoh — detail venue akan dikonfirmasi.</p>','')
    s=s.replace('<button class="button button-outline" @click="addressOpen = true">','<button v-if="wedding.giftAddress" class="button button-outline" @click="addressOpen = true">')
    path.write_text(s,encoding='utf-8')
# Remove duplicate legacy files from the new frontend, leaving the original root project intact.
for path in (root/'components').glob('*.vue'):
    if path.name not in ['BaseModal.vue','BaseToast.vue','WeddingRenderer.vue']:
        assert path.resolve().is_relative_to(root.resolve())
        path.unlink()
for path in [root/'data'/'wedding.js',root/'services'/'storage.js',root/'utils'/'calendar.js']:
    if path.exists():path.unlink()
print('Hardcoded demo content removed from the active template.')
