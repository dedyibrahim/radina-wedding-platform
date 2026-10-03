from pathlib import Path
import json
root=Path('.')
def write(path,s):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def edit(path,a,b):
 p=Path(path);s=p.read_text(encoding='utf-8');assert a in s,path+' missing '+a[:40];p.write_text(s.replace(a,b),encoding='utf-8')
# Keep the existing platform, data, and credential configuration.
for directory in ['frontend/src','backend/database/seeders','frontend/index.html']:
 paths=Path(directory).rglob('*') if Path(directory).is_dir() else [Path(directory)]
 for p in paths:
  if p.is_file() and p.suffix in ['.vue','.js','.css','.php','.html']:
   s=p.read_text(encoding='utf-8');s=s.replace('Everafter','Radina').replace('hello@everafter.test','hello@radina.test');p.write_text(s,encoding='utf-8')
write('backend/database/migrations/2026_10_03_000003_radina_gift_methods.php', '''<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;
use App\Models\WeddingGiftMethod;
return new class extends Migration {
 public function up(): void {
  Schema::table('templates',function(Blueprint $table){$table->string('template_key',80)->default('romantic-floral');});
  Schema::create('wedding_gift_methods',function(Blueprint $table){
   $table->id();$table->foreignId('wedding_id')->constrained()->cascadeOnDelete();$table->string('type',16);
   $table->string('provider',120)->nullable();$table->text('account_number')->nullable();$table->string('account_name',120)->nullable();
   $table->text('logo')->nullable();$table->text('qr_image')->nullable();$table->string('recipient_name',120)->nullable();
   $table->text('phone')->nullable();$table->text('address')->nullable();$table->text('description')->nullable();
   $table->boolean('is_active')->default(true);$table->unsignedInteger('sort_order')->default(0);$table->timestamps();$table->index(['wedding_id','is_active','sort_order']);
  });
  foreach(DB::table('wedding_gifts')->orderBy('id')->get() as $gift){WeddingGiftMethod::create(['wedding_id'=>$gift->wedding_id,'type'=>'BANK','provider'=>$gift->bank,'account_number'=>$gift->account_number,'account_name'=>$gift->account_name,'logo'=>$gift->logo,'is_active'=>true,'sort_order'=>$gift->sort_order]);}
  foreach(DB::table('weddings')->whereNotNull('shipping_gift')->get() as $w){$gift=json_decode($w->shipping_gift,true);if(!empty($gift['address']))WeddingGiftMethod::create(['wedding_id'=>$w->id,'type'=>'PHYSICAL','recipient_name'=>$gift['recipient']??null,'phone'=>$gift['phone']??null,'address'=>$gift['address'],'is_active'=>true,'sort_order'=>100]);}
  foreach(['company_name'=>'Radina','seo_title'=>'Radina — Abadikan Momen Bahagia Anda','seo_description'=>'Radina membantu Anda membuat undangan pernikahan digital yang elegan, modern, personal, dan mudah dibagikan.','footer'=>'Abadikan Momen Bahagia Anda','logo'=>'/brand/radina-logo.svg'] as $key=>$value)DB::table('system_settings')->updateOrInsert(['key'=>$key],['value'=>$value]);
  DB::table('system_settings')->where('key','email')->where('value','hello@everafter.test')->update(['value'=>'hello@radina.test']);
 }
 public function down(): void {Schema::dropIfExists('wedding_gift_methods');Schema::table('templates',fn(Blueprint $table)=>$table->dropColumn('template_key'));}
};
''')
write('backend/app/Models/WeddingGiftMethod.php', '''<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class WeddingGiftMethod extends Model {
 protected $fillable=['wedding_id','type','provider','account_number','account_name','logo','qr_image','recipient_name','phone','address','description','is_active','sort_order'];
 protected function casts(): array {return ['is_active'=>'boolean','sort_order'=>'integer','account_number'=>'encrypted','phone'=>'encrypted','address'=>'encrypted'];}
 public function wedding(){return $this->belongsTo(Wedding::class);}
}
''')
write('backend/app/Http/Requests/SaveGiftRequest.php', '''<?php
namespace App\Http\Requests;
use App\Rules\SafeMediaUrl;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
class SaveGiftRequest extends FormRequest {
 public function authorize(): bool {return (bool)$this->user()?->admin?->active;}
 public function rules(): array {
  $type=$this->input('type');$number=in_array($type,['BANK','EWALLET']);
  return ['type'=>['required',Rule::in(['BANK','EWALLET','QRIS','PHYSICAL'])],
   'provider'=>[Rule::requiredIf($number||$type==='QRIS'),'nullable','string','max:120'],
   'account_number'=>[Rule::requiredIf($number),'nullable','string','max:60','regex:/^[0-9 +().-]+$/'],
   'account_name'=>[Rule::requiredIf($number||$type==='QRIS'),'nullable','string','max:120'],
   'logo'=>['nullable','string','max:2048',new SafeMediaUrl],
   'qr_image'=>[Rule::requiredIf($type==='QRIS'),'nullable','string','max:2048',new SafeMediaUrl],
   'recipient_name'=>[Rule::requiredIf($type==='PHYSICAL'),'nullable','string','max:120'],
   'phone'=>[Rule::requiredIf($type==='PHYSICAL'),'nullable','string','max:30'],
   'address'=>[Rule::requiredIf($type==='PHYSICAL'),'nullable','string','max:2000'],
   'description'=>'nullable|string|max:2000','is_active'=>'required|boolean','sort_order'=>'sometimes|integer|min:0|max:1000'];
 }
}
''')
write('backend/app/Http/Controllers/AdminGiftController.php', '''<?php
namespace App\Http\Controllers;
use App\Models\Wedding;
use App\Models\WeddingGiftMethod;
use App\Http\Requests\SaveGiftRequest;
use App\Services\WeddingService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
class AdminGiftController extends Controller {
 public function __construct(private WeddingService $service){}
 public function index(Wedding $wedding){$this->service->ensurePaid($wedding->order);return response()->json(['data'=>$wedding->giftMethods]);}
 public function store(SaveGiftRequest $request,Wedding $wedding){return DB::transaction(function()use($request,$wedding){$wedding=Wedding::lockForUpdate()->findOrFail($wedding->id);$this->service->ensurePaid($wedding->order);$data=$request->validated();$data['sort_order']??=($wedding->giftMethods()->max('sort_order')??-1)+1;abort_if($wedding->giftMethods()->count()>=30,422,'Maksimal 30 metode hadiah.');$gift=$wedding->giftMethods()->create($data);$wedding->touch();return response()->json(['data'=>$gift,'updated_at'=>$wedding->updated_at],201);});}
 public function update(SaveGiftRequest $request,Wedding $wedding,WeddingGiftMethod $gift){return DB::transaction(function()use($request,$wedding,$gift){$wedding=Wedding::lockForUpdate()->findOrFail($wedding->id);$this->service->ensurePaid($wedding->order);abort_unless($gift->wedding_id===$wedding->id,404);$gift->update($request->validated());$wedding->touch();return response()->json(['data'=>$gift->fresh(),'updated_at'=>$wedding->updated_at]);});}
 public function destroy(Wedding $wedding,WeddingGiftMethod $gift){return DB::transaction(function()use($wedding,$gift){$wedding=Wedding::lockForUpdate()->findOrFail($wedding->id);$this->service->ensurePaid($wedding->order);abort_unless($gift->wedding_id===$wedding->id,404);$gift->delete();$wedding->touch();return response()->json(['message'=>'Metode hadiah dihapus.','updated_at'=>$wedding->updated_at]);});}
 public function reorder(Request $request,Wedding $wedding){$data=$request->validate(['ids'=>'required|array|min:1|max:30','ids.*'=>'required|integer|distinct']);return DB::transaction(function()use($data,$wedding){$wedding=Wedding::lockForUpdate()->findOrFail($wedding->id);$this->service->ensurePaid($wedding->order);$actual=$wedding->giftMethods()->pluck('id')->sort()->values()->all();$supplied=collect($data['ids'])->sort()->values()->all();abort_unless($actual===$supplied,422,'Urutan harus mencakup semua metode hadiah undangan ini.');foreach($data['ids'] as $index=>$id)$wedding->giftMethods()->where('id',$id)->update(['sort_order'=>$index]);$wedding->touch();return response()->json(['data'=>$wedding->fresh()->giftMethods,'updated_at'=>$wedding->updated_at]);});}
}
''')
edit('backend/app/Models/Wedding.php','    public function gifts()',"    public function giftMethods() { return $this->hasMany(WeddingGiftMethod::class)->orderBy('sort_order')->orderBy('id'); }\n\n    public function gifts()")
edit('backend/app/Models/Wedding.php',"'gallery', 'gifts', 'settings'","'gallery', 'gifts', 'giftMethods', 'settings'")
edit('backend/app/Http/Resources/WeddingResource.php',"'template' => new TemplateResource", "'gift_methods' => $request->is('api/admin/*') ? $this->giftMethods : $this->giftMethods->where('is_active', true)->values(),\n            'template' => new TemplateResource")
edit('backend/app/Models/Template.php',"'component_name',", "'component_name', 'template_key',")
edit('backend/app/Http/Resources/TemplateResource.php',"'component_name' => $this->component_name,", "'component_name' => $this->component_name, 'template_key' => $this->template_key,")
edit('backend/routes/api.php',"use App\\Http\\Controllers\\AdminOrderController;","use App\\Http\\Controllers\\AdminGiftController;\nuse App\\Http\\Controllers\\AdminOrderController;")
edit('backend/routes/api.php',"    Route::get('/weddings/{wedding}/rsvps'", "    Route::get('/weddings/{wedding}/gifts', [AdminGiftController::class, 'index']);\n    Route::post('/weddings/{wedding}/gifts', [AdminGiftController::class, 'store']);\n    Route::patch('/weddings/{wedding}/gifts/reorder', [AdminGiftController::class, 'reorder']);\n    Route::put('/weddings/{wedding}/gifts/{gift}', [AdminGiftController::class, 'update']);\n    Route::delete('/weddings/{wedding}/gifts/{gift}', [AdminGiftController::class, 'destroy']);\n    Route::get('/weddings/{wedding}/rsvps'")
edit('backend/app/Http/Controllers/MediaController.php',"'logo', 'video'","'logo', 'video', 'gift'")
# Stable wedding identity, independent of section hashes and guest query strings.
edit('frontend/src/pages/public/Wedding.vue',"watch(() => route.fullPath, load, { immediate: true })", "watch(() => [route.params.id || '', route.params.slug || '', Boolean(route.meta.preview)].join(':'), load, { immediate: true })")
edit('frontend/src/router/index.js',"    return saved ||", "    if (to.path === from.path && (to.path.startsWith('/w/') || to.meta.preview)) return false\n    return saved ||")
edit('frontend/src/router/index.js',"    { path: '/admin/login'", "    { path: '/admin/weddings/:id/preview', component: () => import('../pages/public/Wedding.vue'), meta: { admin: true, preview: true } },\n    { path: '/admin/login'")
edit('frontend/src/router/index.js',"        { path: 'weddings/:id',", "        { path: 'weddings/:id/gift', component: () => import('../pages/admin/WeddingEditor.vue'), meta: { section: 'gift' } },\n        { path: 'weddings/:id',")
write('frontend/src/composables/useSectionNavigation.js', '''export const sectionKeys = ['home','couple','story','event','gallery','gift','rsvp','wishes','closing','date']
export function scrollToSection(key) {
 if (!sectionKeys.includes(key)) return
 document.getElementById(key)?.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',block:'start'})
}
''')
# SVG logo: heart-shaped petals, a subtle R stem, classic wordmark.
symbol='''<g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M30 40C10 30 7 15 15 11C22 7 29 15 30 20C31 15 38 7 45 11C53 15 50 30 30 40Z"/><path d="M30 40V53M23 53V26C34 20 43 29 34 34H23M31 34L40 53"/><path d="M17 45C9 42 8 36 9 32C17 34 21 39 17 45ZM43 45C51 42 52 36 51 32C43 34 39 39 43 45Z"/></g>'''
for name,color in [('radina-logo','#6D4036'),('radina-logo-dark','#2C1B18'),('radina-logo-white','#FFFFFF')]:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 255 66" role="img" aria-label="Radina Digital Wedding Invitation" style="color:{color}">{symbol}<text x="69" y="39" fill="currentColor" font-family="Georgia,serif" font-size="38" letter-spacing="1">Radina</text><text x="71" y="56" fill="currentColor" font-family="Arial,sans-serif" font-size="6.8" letter-spacing="1.5">DIGITAL WEDDING INVITATION</text></svg>'''
 write(f'frontend/src/assets/brand/{name}.svg',svg);write(f'frontend/public/brand/{name}.svg',svg)
icon=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" style="color:#6D4036">{symbol}</svg>'
write('frontend/src/assets/brand/radina-icon.svg',icon);write('frontend/public/brand/radina-icon.svg',icon);write('frontend/public/favicon.svg',icon)
write('frontend/src/components/RadinaLogo.vue','''<script setup>
import primary from '../assets/brand/radina-logo.svg'
import white from '../assets/brand/radina-logo-white.svg'
import icon from '../assets/brand/radina-icon.svg'
defineProps({light:Boolean,iconOnly:Boolean})
</script><template><img :src="iconOnly ? icon : light ? white : primary" alt="Radina — Digital Wedding Invitation" class="radina-logo" :class="{'radina-icon':iconOnly}" /></template>
''')
for path in ['frontend/src/layouts/PublicLayout.vue','frontend/src/layouts/AdminLayout.vue','frontend/src/pages/admin/Login.vue']:
 p=Path(path);s=p.read_text();s=s.replace('<script setup>','<script setup>\nimport RadinaLogo from '+("'../../components/RadinaLogo.vue'" if '/pages/' in path else "'../components/RadinaLogo.vue'"))
 import re
 s=re.sub(r'<img v-if="platform.settings.logo".*?\}\}', '<RadinaLogo />',s,flags=re.S)
 s=s.replace('<span>digital invitations</span>','');p.write_text(s,encoding='utf-8')
edit('frontend/src/components/PageState.vue','<script setup>','<script setup>\nimport RadinaLogo from \'./RadinaLogo.vue\'')
edit('frontend/src/components/PageState.vue','><div class="skeleton skeleton-title">','><RadinaLogo iconOnly /><div class="skeleton skeleton-title">')
edit('frontend/src/components/PaymentInstructions.vue','<script setup>','<script setup>\nimport RadinaLogo from \'./RadinaLogo.vue\'')
# Put the logo inside the existing root container.
p=Path('frontend/src/components/PaymentInstructions.vue');s=p.read_text();s=s.replace('Halo Admin,','Halo Admin Radina,').replace('konfirmasi pembayaran Undangan Digital.','konfirmasi pembayaran pesanan Undangan Digital Radina.');s=s.replace('<template>','<template>\n  <RadinaLogo />',1);p.write_text(s)
edit('frontend/src/pages/public/Home.vue','FOR YOUR ONCE-IN-A-LIFETIME MOMENT','RADINA · DIGITAL WEDDING INVITATION')
edit('frontend/src/pages/public/Home.vue','Setiap kisah cinta pantas dirayakan dengan indah. Hadirkan undangan yang personal, elegan,\n          dan dekat di hati.','Radina membantu Anda membuat undangan pernikahan digital yang elegan, modern, personal, dan mudah dibagikan.')
edit('frontend/src/pages/public/Home.vue','    <div class="benefit-strip">','    <section class="p-section p-container radina-gift-intro"><p class="p-eyebrow">WEDDING GIFT</p><h2>Tanda kasih,<br/><em>langsung untuk mempelai.</em></h2><p>Hadirkan rekening bank, e-wallet, QRIS, dan alamat hadiah dalam satu undangan. Tamu dapat menyalin nomor atau mengunduh QR. Transfer dilakukan melalui aplikasi masing-masing; Radina tidak menerima atau menyimpan dana hadiah.</p></section>\n    <div class="benefit-strip">')
# Radina brand palette only applies to the platform, independently of wedding themes.
p=Path('frontend/src/assets/styles/platform.css');s=p.read_text();mapping={'#344535':'#2c1b18','#51684c':'#6d4036','#8a9081':'#8a6e65','#e1e4d8':'#e8d6c4','#fbfaf5':'#fff9f5','#8b947b':'#b97a6b','#8a967b':'#b97a6b','#f2f4e9':'#f4e8df','#51684c':'#6d4036','#f1f3e9':'#f8eee6'}
for a,b in mapping.items():s=s.replace(a,b)
s+='''\n.brand .radina-logo,.radina-logo{width:166px;height:auto;max-width:100%;object-fit:contain}.radina-logo.radina-icon{width:42px}.brand{gap:0}.radina-gift-intro{max-width:740px;text-align:center}.radina-gift-intro p{max-width:610px;margin:20px auto}.preview-controls{display:flex;gap:6px;flex-wrap:wrap;padding:10px;background:#fff9f5;color:#6d4036;position:sticky;top:0;z-index:40}.preview-controls button{padding:8px 12px;border:1px solid #e8d6c4;border-radius:20px;background:white;font-size:12px;min-height:40px}.template-choice-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:16px}.template-choice img{width:100%;aspect-ratio:4/3;object-fit:cover}.template-choice{border:1px solid #e8d6c4;padding:12px;border-radius:12px}.template-choice h3{font-size:23px}.template-choice .p-button{margin-top:8px;width:100%}.gift-edit-actions{display:flex;gap:8px;flex-wrap:wrap}.gift-edit-actions button{min-height:44px}.gift-qr-preview{width:160px;max-width:100%;height:auto}.radina-gift-tabs{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin:26px 0}.radina-gift-tabs button{border:1px solid var(--gold);color:inherit;background:transparent;padding:10px 14px;border-radius:25px;min-height:44px;font-size:12px}.radina-gift-tabs button.active{background:var(--ink);color:var(--ivory)}.gift-section .bank-card{overflow-wrap:anywhere}.gift-provider-logo{max-width:70px;max-height:30px;object-fit:contain}.gift-qr{width:min(100%,240px);height:auto;display:block;margin:15px auto}.gift-description{font-size:13px}.gift-section{scroll-margin-top:90px}\n''';p.write_text(s,encoding='utf-8')
