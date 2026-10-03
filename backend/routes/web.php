<?php

use App\Http\Controllers\SiteController;
use Illuminate\Support\Facades\Route;

Route::get('/assets/{file}', [SiteController::class, 'asset']);
Route::get('/favicon.svg', fn () => response()->file(base_path('../frontend/public/favicon.svg'), ['Content-Type' => 'image/svg+xml']));
Route::get('/brand/{file}', [SiteController::class, 'brand']);
Route::get('/images/templates/{file}', [SiteController::class, 'thumbnail']);
Route::get('/w/{slug}', [SiteController::class, 'wedding']);
Route::get('/{any?}', [SiteController::class, 'index'])->where('any', '^(?!api(?:/|$)|storage(?:/|$)|sanctum(?:/|$)|assets(?:/|$)).*');
