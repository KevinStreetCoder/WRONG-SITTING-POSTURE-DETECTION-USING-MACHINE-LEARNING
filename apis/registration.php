<?php
require_once "apis.php";

try{
    if($_SERVER['REQUEST_METHOD']=='POST'){
        $username = $_POST['username'];
        $email = $_POST['email'];
        $password = $_POST['password'];
        echo registration($username,$email,$password);
    }else{
        echo "Invalid Request";
    }
}catch(PDOException $e){
    die("ERROR: Could not able to execute $sql. " . $e->getMessage());
}
?>