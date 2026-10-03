# Radina — Wedding Invitation CMS

Vue 3 + Laravel 12 + MySQL. A working Phase 1 platform: marketplace → order → manual transfer / WhatsApp → admin payment verification → wedding CMS → preview → publish → public RSVP and wishes.

The original invitation has been preserved. The active platform lives in `frontend/` and `backend/`.

## Local URLs

- Platform: http://localhost:5173
- Admin: http://localhost:5173/admin/login
- Template preview: http://localhost:5173/templates/romantic-floral/preview
- Laravel API: http://localhost:8000/api/templates
- Production-style server-rendered metadata: http://localhost:8000/w/demo-romantic-floral

Local admin seed: `admin@everafter.test` / `ChangeMe!2026`. This is a development credential: replace `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `backend/.env` before deployment. The seeder does not overwrite an existing user's password.

## Install and run

Requirements: Node.js 20.19+ or 22.12+, PHP 8.2+ with PDO MySQL, GD, fileinfo, mbstring, curl, intl and OpenSSL, Composer, MySQL 8.

```sh
npm install
cd backend
composer install
cp .env.example .env
```

Create a dedicated MySQL database, then configure `DB_*`, `APP_URL`, `FRONTEND_URL`, `SANCTUM_STATEFUL_DOMAINS`, `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `backend/.env`.

```sh
php artisan key:generate
php artisan migrate --seed
php artisan storage:link
php artisan serve --host=127.0.0.1 --port=8000
```

In a second terminal from the project root:

```sh
npm run dev
```

PowerShell users can use `Copy-Item .env.example .env` instead of `cp`; if script execution policy blocks npm, use `npm.cmd`.

This workspace has an isolated local MySQL instance on `127.0.0.1:3307`, with data under `backend/storage/local-mysql`. It does not modify Laragon's existing data directory. Its generated app credentials are stored in the ignored `.env`. To restart that existing instance on this machine:

```powershell
& 'C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysqld.exe' --defaults-file='C:/My Project/weddingWebsite/backend/storage/local-mysql/my.ini' --console
```

Do not run the original scaffolding scripts again on an established installation; they are development construction helpers, not migration tools.

## Using the platform

1. Open `/templates`, preview Romantic Floral, and select it.
2. Fill customer and couple details, review, and create the order. The server determines the price, reserves the slug, and generates the order number.
3. Transfer to the configured bank account. The WhatsApp link prepares a confirmation message; clicking it does not mark payment PAID or send a message automatically. The customer sends the transfer receipt in WhatsApp.
4. Admin opens the order, verifies the transfer, and confirms payment. Payment records retain `confirmed_by`, `confirmed_at`, and optional reference.
5. Click **Kelola Undangan**. The system creates a wedding only for a paid, valid order.
6. Edit basic details, couple photos, multiple events, story, gallery, music, gifts, livestream, and feature settings. Save changes. Unsaved changes are indicated; leaving the editor prompts before discarding them.
7. Preview uses the real saved database content and requires the admin session.
8. Publish validates couple names, wedding date, at least one event, template, and slug. Share `/w/{slug}?to=Nama%20Tamu`.
9. Guest RSVP and wishes are stored in MySQL. Admin can review RSVPs and hide/show wishes in the editor.

The seeded WhatsApp number, bank details, couple identities, photos, venue, and gifts are demo content. Configure real platform bank details and WhatsApp under `/admin/settings` before accepting payments. Empty the payment notice only after the details are verified.

## Structure

```text
frontend/src/
  components/      reusable forms, uploaders, modals, template renderer
  layouts/         public navigation and responsive admin workspace
  pages/public/    home, marketplace, template detail, order, check order, wedding
  pages/admin/     auth, dashboard, orders, CMS, templates, system settings
  router/          lazy-loaded routes and admin navigation guard
  stores/          Pinia authentication, platform config, notifications
  services/        Axios API client with Sanctum CSRF/session handling
  templates/RomanticFloral/
                   complete invitation and animated floral components
  utils/weddingView.js
                   presentation adapter for the shared wedding contract
backend/
  app/Http/Requests/   server-side validation
  app/Http/Resources/  public/admin JSON contracts
  app/Services/       order workflow, payment, wedding persistence/publish
  app/Models/         relational Eloquent models
  database/           migrations and seed data
  routes/             API routes and production SPA/metadata delivery
```

Templates receive the same `wedding` prop; `WeddingRenderer.vue` uses an explicit component whitelist. Twenty visual templates share the same CMS and API contract. Admin can manage catalog entries using the registered components; adding another visual template requires a developer component and updating the whitelist and validation rule. Disabling a template prevents new orders and preserves existing published invitations.

API content, not localStorage, drives the platform. SessionStorage only retains the customer's order lookup WhatsApp within their own browser tab; order/payment/content remain on the server.

## API

Public: `GET /api/settings`, `/categories`, `/templates`, `/templates/{slug}`, `/templates/{slug}/preview`; `POST /api/orders`, `/check-order`, `/orders/payment-review`; `GET /api/weddings/{slug}`, `/weddings/{slug}/wishes`; `POST /api/weddings/{slug}/rsvp`, `/weddings/{slug}/wishes`.

Auth: `/sanctum/csrf-cookie`, `POST /api/admin/login`, `GET /api/admin/me`, `POST /api/admin/logout`. The first-party SPA uses Sanctum cookie sessions and CSRF, not browser-stored bearer tokens.

Admin: `GET /api/admin/dashboard`, `/orders`, `/orders/{id}`; `PATCH /orders/{id}/payment`, `/orders/{id}/status`; `POST /orders/{id}/wedding`; `GET/PUT /weddings/{id}`; `GET /weddings/{id}/preview`; `POST /weddings/{id}/publish`; `GET /weddings/{id}/rsvps`, `/weddings/{id}/wishes`; `PATCH /weddings/{id}/wishes/{wish}`; `POST /media`; `GET/POST /templates`, `PUT /templates/{id}`; `GET/PUT /settings` (all admin paths prefixed by `/api/admin`).

Mutating editor requests include `expected_updated_at`; concurrent updates return 409 instead of overwriting another session's changes. Child collections use explicit field whitelists and transactionally preserve their sort order. Financial prices are integer IDR snapshots, not client-submitted totals.

Uploads generate UUID filenames. Images are validated by detected MIME, pixel count, and size, decoded and compressed to WebP up to 1600px. Music allows MP3/WAV/OGG; local videos allow MP4. A gallery/portrait delete removes the reference from the wedding when saved; unreferenced media files are retained rather than deleting files still potentially in use. Storage cleanup/retention policies can be added separately.

## Testing

Create a separate `wedding_cms_test` database with the same app user's permissions. PHPUnit is explicitly configured for this database and checks its name before resetting test tables; never point tests at production data.

```sh
cd backend
php artisan test --filter=PlatformWorkflowTest
```

Browser tests use the installed Chrome browser, real MySQL, and the local Vite/API servers:

```sh
npm run test:e2e
```

They create clearly named test orders, verify the real customer/admin/guest journey, media uploads, preview restrictions, publication, and server persistence, then check public/admin/wedding routes at ten target widths (320–1440px). Screenshots and reports are under `test-results/platform/`.

## Build and deployment

```sh
npm run build
cd backend
composer install --no-dev --optimize-autoloader
php artisan migrate --force
php artisan storage:link
php artisan config:cache
php artisan route:cache
```

Serve `backend/public` as the web document root. Laravel delivers the built Vue SPA and compiled `/assets` files. Public `/w/{slug}` HTML includes database-driven title, description, OpenGraph cover, and canonical URL before JavaScript runs, so social sharing works without executing Vue. Use the same public origin for SPA and API; set `APP_URL` and `FRONTEND_URL` to that HTTPS origin, configure Sanctum's stateful domain, `APP_ENV=production`, `APP_DEBUG=false`, and `SESSION_SECURE_COOKIE=true`.

Seed initially with explicitly configured administrator credentials (`php artisan db:seed --force`). Back up the database and `storage/app/public`. Shared host configuration and HTTPS/public domain are required before real guests can reach the site; localhost links are for development only. No payment gateway, customer accounts, bulk messaging, custom domains, or analytics are implemented; those remain Phase 2.

Photo and music credits: `frontend/public/ASSET-CREDITS.md`.


## Radina upgrade

This upgrade continues the existing installation. Run `php artisan migrate` then `php artisan db:seed --class=RadinaSeeder` in backend; neither command resets customer data. Existing bank gifts and shipping addresses migrate to encrypted `wedding_gift_methods`. Keep APP_KEY unchanged: changing it makes encrypted gift data unreadable. Administrator credentials remain unchanged.

The original ten template keys are: romantic-floral, elegant-luxury, minimalist-white, nusantara-heritage, garden-dream, classic-vintage, midnight-romance, sakinah, eternal-story, blush. Components in `frontend/src/templates/*/index.vue` share WeddingExperience, RSVP, wishes, audio, countdown, gallery and gift behavior. Each folder now contains its own Opening.vue, Hero.vue, presentation.css, and theme.css. Shared presentation components render alternating portraits, editorial tickets, calendar events, numbered stories, scrapbook chapters, and immersive cinematic chapters. Styles and components load through the selected registry entry. Marketplace thumbnails are captures of the rendered covers; each live demo has a different fictional couple and content.

Gift CMS: `/admin/weddings/{id}/gift`. BANK, EWALLET, QRIS and PHYSICAL methods have independent active status and order. Gift changes save immediately via their dedicated endpoints; the wedding editor's Save applies the enable switch and other wedding content. Public JSON includes only active gift_methods. Account numbers, phone numbers and shipping addresses use Laravel encrypted casts at rest. These intentional gift destinations are displayed to guests when enabled; Radina holds no guest funds, and no unverified app deep links are generated.

GET/POST `/api/admin/weddings/{id}/gifts`; PUT/DELETE `/gifts/{giftId}`; PATCH `/gifts/reorder` accepts all method IDs in desired order. Cross-wedding gift IDs return 404. All writes require an active admin and a paid order.

Preview bug root cause: Wedding.vue watched route.fullPath and reset wedding to null on hash changes; that unmounted WeddingRenderer and reset opening/audio. It now watches only wedding identity, renderer no longer keys by updated_at, and section buttons call scrollIntoView with semantic keys without changing URL/query. Audio lives in the persistent renderer. Admin preview route `/admin/weddings/{id}/preview` starts opened and provides explicit Preview Cover; the editor's live preview reacts to unsaved content without remounting after each edit.

Run `node scripts/radina-test.mjs` for 10-template/10-viewport regression coverage and preview navigation/music state checks. Original end-to-end customer/payment/publish tests remain in `scripts/platform-test.mjs`.

The four SVG logo variants are in `frontend/src/assets/brand/` and `frontend/public/brand/`. Logo artwork and catalog SVG illustrations are created for this project; existing photography/music credits remain in ASSET-CREDITS.md.


## Distinct experiences and Music Library upgrade

This is an additive upgrade. Back up the database and storage, keep the existing APP_KEY, then run:

```sh
cd backend
php artisan migrate
php artisan db:seed --class=ExperienceSeeder
```

The seeders now install twenty fictional demo invitations and fifty original instrumental demo cues. It preserves existing customer invitations, prices, template visibility, orders, payments, RSVP, and wishes. New assets are checked into `frontend/public/images/demos`, `frontend/public/images/templates/previews`, and `frontend/public/music/library`; the seeder copies them to Laravel public storage. A fresh `DatabaseSeeder` invokes both catalog and experience seeders. No asset-generation tools are needed to run the application.

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

Browser tests use installed Google Chrome. Experience tests cover 200 template/viewport combinations, image integrity, long guest names, semantic navigation, and one persistent audio element. Music CMS tests cover the real UI, playlist persistence, shuffle, section headings/order, and live preview; changes to the demonstration invitation are restored afterwards. Backend tests run only against the isolated `wedding_cms_test` database. Photography and music provenance is recorded in `frontend/public/ASSET-CREDITS.md`; demonstration couples are fictional.


## Upgrade: 20-template collection

RADINA now includes twenty developer-managed designs, a 50-track original demo music library, eleven marketplace categories, persistent favorites, and comparison of up to three templates. Existing customer data and payment flow remain unchanged. See [the upgrade guide](docs/TWENTY-TEMPLATES.md) for the new collection, setup commands, architecture, asset notes and tests.

# radina-wedding-platform
