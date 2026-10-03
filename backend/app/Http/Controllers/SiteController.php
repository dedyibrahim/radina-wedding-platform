<?php

namespace App\Http\Controllers;

use App\Models\Wedding;
use App\Services\PlatformSettings;
use Illuminate\Http\Request;

class SiteController extends Controller
{
    public function index(Request $request, PlatformSettings $settings)
    {
        return $this->html($settings->all());
    }

    public function wedding(Request $request, string $slug, PlatformSettings $settings)
    {
        $w = Wedding::where('slug', $slug)->where('status', 'PUBLISHED')->whereHas('order', fn ($q) => $q->where('status', 'PUBLISHED')->whereHas('payment', fn ($p) => $p->where('status', 'PAID')))->first();
        if (! $w) {
            return $this->html($settings->all(), null, 404);
        }

        return $this->html($settings->all(), $w);
    }

    private function html(array $settings, ?Wedding $w = null, int $status = 200)
    {
        $path = base_path('../frontend/dist/index.html');
        if (! file_exists($path)) {
            return response('Build frontend with npm run build, or use the Vite development server.', 503);
        }
        $html = file_get_contents($path);
        $title = $w?->title ?? $settings['seo_title'] ?? $settings['company_name'] ?? 'Wedding Invitation';
        $description = $w ? ($w->wedding_date?->format('d F Y').' — '.$w->opening_text) : ($settings['seo_description'] ?? '');
        $image = $w?->cover_image ?? '';
        if (str_starts_with($image, '/')) {
            $image = rtrim(config('app.url'), '/').$image;
        }
        $html = preg_replace_callback('#<title>.*?</title>#s', fn () => '<title>'.e($title).'</title>', $html);
        foreach (['description' => $description, 'og:title' => $title, 'og:description' => $description, 'og:image' => $image] as $name => $value) {
            $attribute = str_starts_with($name, 'og:') ? 'property' : 'name';
            $tag = '<meta '.$attribute.'="'.$name.'" content="'.e($value).'" />';
            $pattern = '#<meta '.$attribute.'="'.preg_quote($name, '#').'"[^>]*>#';
            if (preg_match($pattern, $html)) {
                $html = preg_replace_callback($pattern, fn () => $tag, $html);
            } else {
                $html = str_replace('</head>', $tag.'</head>', $html);
            }
        }
        $html = str_replace('</head>', '<link rel="canonical" href="'.e(url($w ? '/w/'.$w->slug : '/')).'" /></head>', $html);

        return response($html, $status)->header('Content-Type', 'text/html; charset=UTF-8')->header('X-Content-Type-Options', 'nosniff');
    }

    public function brand(string $file)
    {
        return $this->publicSvg('brand', $file);
    }

    public function thumbnail(string $file)
    {
        return $this->publicSvg('images/templates', $file);
    }

    private function publicSvg(string $directory, string $file)
    {
        abort_unless(preg_match('/^[a-z0-9-]+\.svg$/', $file), 404);
        $path = base_path('../frontend/public/'.$directory.'/'.$file);
        abort_unless(is_file($path), 404);

        return response()->file($path, ['Content-Type' => 'image/svg+xml', 'Cache-Control' => 'public, max-age=3600', 'X-Content-Type-Options' => 'nosniff']);
    }

    public function asset(string $file)
    {
        abort_unless(preg_match('/^[a-zA-Z0-9_\-.]+\.(js|css|woff2|svg)$/', $file), 404);
        $path = base_path('../frontend/dist/assets/'.$file);
        abort_unless(is_file($path), 404);
        $type = match (pathinfo($file, PATHINFO_EXTENSION)) {
            'js' => 'application/javascript','css' => 'text/css','woff2' => 'font/woff2',default => 'image/svg+xml'
        };

        return response()->file($path, ['Content-Type' => $type, 'Cache-Control' => 'public, max-age=31536000, immutable', 'X-Content-Type-Options' => 'nosniff']);
    }
}
