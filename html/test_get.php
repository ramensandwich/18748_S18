<?php
$url = 'http://3e250a62.ngrok.io/18748_get.php?day=Fri&hour=11&query=rec';
$data = http_build_query(array('loc' => 'sorrels','date' => '4-17-2018'));

// use key 'http' even if you send the request to https://...
//$options = array(
//    'http' => array(
//        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
//        'method'  => 'GET',
//        'content' => $data
//    )
//);
//$context  = stream_context_create($options);
$result = file_get_contents($url);
if ($result === FALSE) { /* Handle error */ }

var_dump($result);


?>
