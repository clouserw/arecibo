<?php 
function post($url, $data) {
    $ch = curl_init();
    $data_string = http_build_query($data);
    curl_setopt($ch, CURLOPT_URL, $url);  
    curl_setopt($ch, CURLOPT_POST, count($data));  
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    $result = curl_exec($ch);  
    curl_close($ch);
}
?>