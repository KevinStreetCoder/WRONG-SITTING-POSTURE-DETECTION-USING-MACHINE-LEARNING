<?php
    include "apis.php";

    $server_link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
    // echo $server_link;

    session_start();
    $user_id = $_SESSION['id'];

    echo start_model($server_link, $user_id);

?>