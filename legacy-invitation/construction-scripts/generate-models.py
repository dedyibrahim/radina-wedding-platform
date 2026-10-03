from pathlib import Path
root=Path(__file__).resolve().parents[1]/'backend'/'app'/'Models'
models={
 'Admin':('admins', ['user_id','active'],"public function user(){return $this->belongsTo(User::class);}","['active'=>'boolean']"),
 'TemplateCategory':('template_categories',['name','slug'],'',None),
 'Payment':('payments',['order_id','payment_method','amount','status','reference','confirmed_by','confirmed_at'],"public function order(){return $this->belongsTo(Order::class);}","['confirmed_at'=>'datetime']"),
 'OrderStatusHistory':('order_status_histories',['order_id','old_status','new_status','changed_by','created_at'],'public $timestamps=false;',None),
 'WeddingCouple':('wedding_couples',['wedding_id','role','full_name','nickname','father_name','mother_name','photo','instagram','family_order'],'',None),
 'WeddingEvent':('wedding_events',['wedding_id','type','title','date','start_time','end_time','timezone','venue','address','google_maps_url','sort_order'],'',None),
 'WeddingStory':('wedding_stories',['wedding_id','date_label','title','description','image','sort_order'],'',None),
 'WeddingGallery':('wedding_galleries',['wedding_id','image','caption','sort_order'],'',None),
 'WeddingGift':('wedding_gifts',['wedding_id','bank','account_number','account_name','logo','sort_order'],'',None),
 'WeddingSetting':('wedding_settings',['wedding_id']+['enable_'+x for x in ['music','gallery','story','rsvp','wishes','gift','livestream','countdown','video','maps']],'',"["+','.join("'enable_"+x+"'=>'boolean'" for x in ['music','gallery','story','rsvp','wishes','gift','livestream','countdown','video','maps'])+"]"),
 'WeddingRsvp':('wedding_rsvps',['wedding_id','name','guests','attendance','message'],'',None),
 'WeddingWish':('wedding_wishes',['wedding_id','name','message','visible'],'',"['visible'=>'boolean']"),
 'Media':('media',['wedding_id','uploaded_by','collection','disk','path','mime_type','size'],'',None),
 'SystemSetting':('system_settings',['key','value'],'',None)
}
for name,(table,fields,extra,casts) in models.items():
    fieldlist=','.join("'"+field+"'" for field in fields)
    content=f"<?php\nnamespace App\\Models;\nuse Illuminate\\Database\\Eloquent\\Model;\nclass {name} extends Model {{\n    protected $table='{table}';\n    protected $fillable=[{fieldlist}];\n    {extra}\n"
    if casts:content+=f"    protected function casts():array{{return {casts};}}\n"
    (root/(name+'.php')).write_text(content+'}\n')
user=root/'User.php'
source=user.read_text()
source=source.replace('use HasFactory, Notifiable;', 'use HasFactory, Notifiable, \\Laravel\\Sanctum\\HasApiTokens;')
source=source.replace('    /**\n     * The attributes that are mass assignable.', '    public function admin(){return $this->hasOne(Admin::class);}\n\n    /**\n     * The attributes that are mass assignable.',1)
user.write_text(source)
print('Relational Eloquent models generated.')
