<?php
include "apis.php";

try{
    if($_SERVER['REQUEST_METHOD']=='POST'){
        $email = $_POST['email'];
        echo forgot($email);
    }else{
        echo "Invalid Request";
    }        
}catch(PDOException $e){
    die("ERROR: Could not able to execute " . $e->getMessage());
}
?>