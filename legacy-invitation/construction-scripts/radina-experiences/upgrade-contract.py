from pathlib import Path
root=Path(__file__).resolve().parents[1]
def edit(path, before, after):
 p=root/path;s=p.read_text(encoding='utf-8');assert before in s, (path,before);p.write_text(s.replace(before,after),encoding='utf-8')
edit('backend/app/Models/Wedding.php', "'is_demo'];", "'is_demo', 'section_content', 'section_order', 'music_playlist', 'music_shuffle', 'music_repeat'];")
edit('backend/app/Models/Wedding.php', "    protected $guarded = [];\n\n", '')
edit('backend/app/Models/Wedding.php', "return ['wedding_date'", "return ['section_content' => 'array', 'section_order' => 'array', 'music_playlist' => 'array', 'music_shuffle' => 'boolean', 'music_repeat' => 'boolean', 'wedding_date'")
edit('backend/app/Http/Resources/WeddingResource.php', "'music' => ['music_url'", "'section_content' => $this->section_content, 'section_order' => $this->section_order,\n            'music' => ['playlist' => $this->music_playlist ?? [], 'shuffle' => $this->music_shuffle, 'repeat' => $this->music_repeat, 'music_url'")
edit('backend/app/Services/WeddingService.php', "'video_url', 'shipping_gift'", "'video_url', 'shipping_gift', 'section_content', 'section_order'")
edit('backend/app/Services/WeddingService.php', '            $wedding->update($base);', '''            if (array_key_exists('playlist', $data['music'])) {
                $playlist = [];
                foreach ($data['music']['playlist'] as $track) {
                    if (! empty($track['library_id'])) {
                        $library = \\App\\Models\\MusicTrack::find($track['library_id']);
                        $saved = collect($wedding->music_playlist ?? [])->firstWhere('library_id', $track['library_id']);
                        if ($library?->is_active) {
                            $playlist[] = ['library_id'=>$library->id,'title'=>$library->title,'artist'=>$library->artist,'url'=>$library->file_url,'cover'=>$library->cover_image,'duration'=>$library->duration];
                        } elseif ($saved) {
                            $playlist[] = $saved;
                        } else {
                            throw ValidationException::withMessages(['music.playlist'=>'Lagu library tidak tersedia.']);
                        }
                    } else {
                        $playlist[] = collect($track)->only(['title','artist','url','cover','duration'])->all();
                    }
                }
                $base['music_playlist'] = $playlist;
            }
            if (array_key_exists('shuffle', $data['music'])) $base['music_shuffle'] = $data['music']['shuffle'];
            if (array_key_exists('repeat', $data['music'])) $base['music_repeat'] = $data['music']['repeat'];
            $wedding->update($base);''')
edit('backend/app/Http/Requests/SaveWeddingRequest.php', "'settings' => 'required|array',", """'settings' => 'required|array',
            'section_content' => 'nullable|array:opening,home,couple,parents,quote,date,story,event,gallery,video,location,gift,rsvp,wishes,livestream,closing',
            'section_content.*' => 'array:enabled,heading,subheading,content',
            'section_content.*.enabled' => 'sometimes|boolean', 'section_content.*.heading' => 'nullable|string|max:255',
            'section_content.*.subheading' => 'nullable|string|max:1000', 'section_content.*.content' => 'nullable|string|max:5000',
            'section_order' => 'nullable|array|max:15',
            'section_order.*' => ['required','distinct',Rule::in(['home','couple','quote','date','story','event','gallery','video','location','gift','rsvp','wishes','livestream','closing'])],
            'music.playlist' => 'sometimes|array|max:10', 'music.playlist.*' => 'array:library_id,title,artist,url,cover,duration',
            'music.playlist.*.library_id' => 'nullable|integer|min:1', 'music.playlist.*.title' => 'required|string|max:255',
            'music.playlist.*.artist' => 'nullable|string|max:255', 'music.playlist.*.url' => ['required','string','max:2048',new SafeMediaUrl],
            'music.playlist.*.cover' => $media, 'music.playlist.*.duration' => 'nullable|integer|min:0|max:7200',
            'music.shuffle' => 'sometimes|boolean', 'music.repeat' => 'sometimes|boolean',""")
edit('backend/app/Http/Controllers/MediaController.php', "'video', 'gift'", "'video', 'gift', 'music-library', 'music-cover'")
edit('backend/app/Http/Controllers/MediaController.php', "['templates', 'logo']", "['templates', 'logo', 'music-library', 'music-cover']")
edit('backend/app/Http/Controllers/MediaController.php', "$collection === 'music'", "in_array($collection, ['music','music-library'])")
edit('frontend/src/components/MediaUploader.vue', "['music', 'video']", "['music', 'music-library', 'video']")
edit('frontend/src/components/MediaUploader.vue', "collection === 'music'", "['music', 'music-library'].includes(collection)")
edit('frontend/src/router/index.js', "{ path: 'templates', component: () => import('../pages/admin/Templates.vue') },", "{ path: 'templates', component: () => import('../pages/admin/Templates.vue') },\n        { path: 'music', component: () => import('../pages/admin/MusicLibrary.vue') },")
edit('frontend/src/layouts/AdminLayout.vue', "  Settings,", "  Settings,\n  Music,")
edit('frontend/src/layouts/AdminLayout.vue', "  { path: '/admin/settings'", "  { path: '/admin/music', name: 'Music Library', icon: Music },\n  { path: '/admin/settings'")
