<?php
include "apis.php";

try{
    if($_SERVER['REQUEST_METHOD']=='POST'){
        $email = $_POST['email'];
        $password = $_POST['password'];
        echo resetPassword($email,$password);
    }else{
        echo "Invalid Request";
    }        
}catch(PDOException $e){
    die("ERROR: Could not able to execute " . $e->getMessage());
}
?>