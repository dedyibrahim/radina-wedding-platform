from pathlib import Path
import json, shutil, secrets

root = Path(__file__).resolve().parents[1]
front = root / 'frontend'
front.mkdir(exist_ok=True)
for directory in ['src', 'public']:
    shutil.copytree(root / directory, front / directory, dirs_exist_ok=True)
shutil.copy2(root / 'index.html', front / 'index.html')
package = json.loads((root / 'package.json').read_text())
package['name'] = 'everafter-frontend'
package['dependencies'].update({'vue-router': '^4.5.0', 'pinia': '^3.0.0', 'axios': '^1.8.0'})
package['scripts'] = {'dev': 'vite --host 0.0.0.0', 'build': 'vite build', 'preview': 'vite preview --host 0.0.0.0'}
(front / 'package.json').write_text(json.dumps(package, indent=2)+'\n')
(root / 'package.json').write_text(json.dumps({
 'name':'everafter-wedding-platform','private':True,'type':'module','workspaces':['frontend'],
 'scripts':{'dev':'npm run dev --workspace frontend','build':'npm run build --workspace frontend','preview':'npm run preview --workspace frontend','dev:api':'php backend/artisan serve --host=127.0.0.1 --port=8000','test:e2e':'node scripts/platform-test.mjs'},
 'devDependencies':{'@playwright/test':'^1.51.0'}
},indent=2)+'\n')
composer = root / 'backend' / 'composer.json'
data = json.loads(composer.read_text())
data['require']['laravel/sanctum'] = '^4.0'
composer.write_text(json.dumps(data,indent=4)+'\n')
env = '''APP_NAME=Everafter
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_TIMEZONE=Asia/Jakarta
FRONTEND_URL=http://localhost:5173
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3307
DB_DATABASE=wedding_cms
DB_USERNAME=wedding_app
DB_PASSWORD={password}
SESSION_DRIVER=file
SESSION_LIFETIME=120
SESSION_DOMAIN=null
SESSION_SECURE_COOKIE=false
SANCTUM_STATEFUL_DOMAINS=localhost:5173,127.0.0.1:5173,localhost:8000,127.0.0.1:8000
CACHE_STORE=file
QUEUE_CONNECTION=sync
FILESYSTEM_DISK=public
LOG_CHANNEL=stack
LOG_LEVEL=debug
ADMIN_EMAIL=admin@everafter.test
ADMIN_PASSWORD=ChangeMe!2026
'''
password=secrets.token_hex(20)
(root/'backend'/'.env').write_text(env.format(password=password))
(root/'backend'/'.env.example').write_text(env.format(password='your-mysql-password').replace('ADMIN_PASSWORD=ChangeMe!2026','ADMIN_PASSWORD=choose-a-strong-password'))
local=root/'backend'/'storage'/'local-mysql'
local.mkdir(parents=True,exist_ok=True)
(local/'my.ini').write_text('[mysqld]\nbasedir=C:/laragon/bin/mysql/mysql-8.0.30-winx64\ndatadir='+str(local/'data').replace('\\','/')+'\nport=3307\nbind-address=127.0.0.1\nmysqlx=0\ncharacter-set-server=utf8mb4\ncollation-server=utf8mb4_unicode_ci\n')
(local/'init.sql').write_text("CREATE DATABASE IF NOT EXISTS wedding_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\nCREATE DATABASE IF NOT EXISTS wedding_cms_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\nCREATE USER IF NOT EXISTS 'wedding_app'@'127.0.0.1' IDENTIFIED BY '"+password+"';\nGRANT ALL PRIVILEGES ON wedding_cms.* TO 'wedding_app'@'127.0.0.1';\nGRANT ALL PRIVILEGES ON wedding_cms_test.* TO 'wedding_app'@'127.0.0.1';\n")
print('Frontend scaffold, Laravel config, and isolated MySQL configuration prepared.')
