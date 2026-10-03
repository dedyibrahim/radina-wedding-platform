from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
(root/'frontend/src/templates/contentPresets.js').write_text("// One developer-managed preset contract, shared with Laravel. CMS overrides are stored separately.\nimport presets from '../../../backend/config/template-presets.json'\nexport const contentPresets = presets\nexport function presetFor(key) { return contentPresets[key] || contentPresets['romantic-floral'] }\n",encoding='utf-8')
p=root/'package.json';data=json.loads(p.read_text(encoding='utf-8'));data['scripts']['test:experiences']='node scripts/experience-test.mjs';data['scripts']['test:music-cms']='node scripts/music-cms-test.mjs';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8');s=s.replace('Visual compositions are defined in themes.css. Catalog thumbnails are original illustrative SVG previews; live previews use the same seeded wedding contract.', 'Each folder now contains its own Opening.vue, Hero.vue, presentation.css, and theme.css. Shared presentation components render alternating portraits, editorial tickets, calendar events, numbered stories, scrapbook chapters, and immersive cinematic chapters. Styles and components load through the selected registry entry. Marketplace thumbnails are captures of the rendered covers; each live demo has a different fictional couple and content.')
s+='''

## Distinct experiences and Music Library upgrade

This is an additive upgrade. Back up the database and storage, keep the existing APP_KEY, then run:

```sh
cd backend
php artisan migrate
php artisan db:seed --class=ExperienceSeeder
```

The seeder adds ten fictional demo invitations and ten original instrumental tracks. It preserves existing customer invitations, prices, template visibility, orders, payments, RSVP, and wishes. New assets are checked into `frontend/public/images/demos`, `frontend/public/images/templates/previews`, and `frontend/public/music/library`; the seeder copies them to Laravel public storage. A fresh `DatabaseSeeder` invokes both catalog and experience seeders. No asset-generation tools are needed to run the application.

| Registry key (stable) | Experience | Composition |
| --- | --- | --- |
| romantic-floral | Amore Bloom | Overlapping editorial photos, alternating portraits, floral vine, masonry |
| elegant-luxury | Noir Élégance | Split opening, fashion masthead, monochrome portraits, admission tickets |
| minimalist-white | Pure | Typography opening, full-bleed photography, calendar, numbered chapters |
| nusantara-heritage | Nusantara | Opening gates, geometric frames, manuscript, formal invitation |
| garden-dream | Verdant Vows | Garden arch, circular portraits, curved path, polaroid board |
| classic-vintage | Heritage Letters | Envelope and letter, photo album, stamps, scrapbook |
| midnight-romance | After Dark | Dramatic photography, glass panels, glowing timeline, swipe gallery |
| sakinah | Sakinah | Bismillah, Islamic arch, prominent quote, symmetrical portraits |
| eternal-story | Frame by Frame | Full-viewport chapters, couple in the story, cinematic reel, film credits |
| blush | Daydream | Pastel blobs, collage, card stack, pastel tickets, playful dock |

Preset source: `backend/config/template-presets.json`, imported directly by the frontend and read by `TemplateContent`. Initial wedding creation applies the selected preset. Switching templates preserves saved text, media, playlist, gifts, and guest records. A null `section_order` uses the current template's recommendation; an explicit saved order stays unchanged. Section Manager can restore the recommendation without overwriting text. In Frame by Frame's recommended layout, couple portraits appear between story chapters; an explicit CMS order uses the administrator's arrangement.

Wedding Editor → Section Manager supports enabled/disabled sections, headings, subheadings, content, desktop drag-and-drop, and accessible reorder buttons usable on touch screens. Hero and opening remain separate. Existing couple/parents, events, media, gift, RSVP/wishes moderation, and publish tabs remain available. Preview responds to editor data. Demo RSVP/wishes can be tried locally in the preview session and never write guest records to the backend.

Music Library: `/admin/music`. GET/POST `/api/admin/music`, PUT/DELETE `/api/admin/music/{id}`. Add licensed or owned audio, upload MP3/WAV/OGG up to 30 MB, add a cover, category, duration, active/featured status, and preview. `music_library` stores catalog metadata. Wedding Editor → Music supports library search/filter, custom uploads, external http/https URLs, and ordered playlists of up to ten tracks, shuffle, repeat, volume, and start-after-opening. Library selections are resolved against server metadata; custom URLs use the existing safe media validator. Removing a library entry does not unlink recordings already used by saved invitation playlists.

One audio element belongs to WeddingRenderer. It starts after an explicit guest interaction, advances on `ended`, and remains unchanged during section navigation and same-path hash/query updates. The compact floating player expands to title/artist/previous/play/next. Music URLs from existing invitations remain a fallback when the playlist is empty. Order payments remain separate from guest gifts.

```sh
npm install
npm run dev
# Separate terminal:
npm run dev:api
# Validation:
npm run build
npm run test:experiences
npm run test:music-cms
cd backend
php artisan test
```

Browser tests use installed Google Chrome. Experience tests cover 100 template/viewport combinations, image integrity, long guest names, semantic navigation, and one persistent audio element. Music CMS tests cover the real UI, playlist persistence, shuffle, section headings/order, and live preview; changes to the demonstration invitation are restored afterwards. Backend tests run only against the isolated `wedding_cms_test` database. Photography and music provenance is recorded in `frontend/public/ASSET-CREDITS.md`; demonstration couples are fictional.
'''
p.write_text(s,encoding='utf-8')
