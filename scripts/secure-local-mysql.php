<?php
// Run only once against the isolated instance created for this project, not a shared MySQL server.
$local=dirname(__DIR__).'/backend/storage/local-mysql';
if(file_exists($local.'/admin-client.ini')){echo "Isolated MySQL root already configured.\n";exit;}
$db=new PDO('mysql:host=127.0.0.1;port=3307','root','',[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
if($db->query('SELECT CURRENT_USER()')->fetchColumn()!=='root@localhost')throw new RuntimeException('Unexpected MySQL root identity.');
$password=bin2hex(random_bytes(32));
file_put_contents($local.'/admin-client.ini',"[client]\nhost=127.0.0.1\nport=3307\nuser=root\npassword=$password\n");
$db->exec("ALTER USER 'root'@'localhost' IDENTIFIED BY '$password'");
echo "Isolated project MySQL root password secured; app connection unchanged.\n";
