<?php
    include "apis.php";

    if($_SERVER['REQUEST_METHOD']=='POST'){
        $user_id = $_POST['user_id'];
        $posture = $_POST['posture'];

        echo update_posture($user_id, $posture);
    }

    
?>