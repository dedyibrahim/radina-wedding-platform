<?php
$root=dirname(__DIR__).'/backend';
$env=parse_ini_file($root.'/.env',false,INI_SCANNER_RAW);
$db=new PDO('mysql:host=127.0.0.1;port=3307','root','',[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
foreach(explode(';',file_get_contents($root.'/storage/local-mysql/init.sql'))as$sql)if(trim($sql)!=='')$db->exec($sql);
$database=$root.'/config/database.php';
$source=file_get_contents($database);
$source=str_replace('PDO::MYSQL_ATTR_SSL_CA',"(defined('Pdo\\\\Mysql::ATTR_SSL_CA') ? constant('Pdo\\\\Mysql::ATTR_SSL_CA') : PDO::MYSQL_ATTR_SSL_CA)",$source);
file_put_contents($database,$source);
$app=$root.'/config/app.php';$source=file_get_contents($app);$source=str_replace("'timezone' => 'UTC'","'timezone' => env('APP_TIMEZONE', 'Asia/Jakarta')",$source);file_put_contents($app,$source);
echo "Dedicated MySQL databases and local configuration ready.\n";
