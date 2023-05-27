<?php

function login($email,$password){
    require ("dbConfig.php");

    $sql = "SELECT * FROM users where (email= '$email' or username= '$email') and password = '$password'";   
    $result = $pdo->query($sql);
    if($result->rowCount() == 1){
        session_start();
        $row = $result->fetch();
        $_SESSION['id'] = $row['id'];
  	    $_SESSION['loggedin'] = true;
        echo "Successfully Logged In";
    }else{
        echo 'Invalid details';
    }
}

function registration($username,$email,$password){
    require ("dbConfig.php");
    
    $sql = "SELECT * FROM users where email= '$email' or username = '$username'";   
    $result = $pdo->query($sql);
    if($result->rowCount() > 0){
        echo 'Email or Username Already Exist';
    }else{
        $sql = "INSERT INTO users (username, email, `password`) values ('$username','$email','$password')";    
        $pdo->exec($sql);
        echo "Registered Successfully";
    }    
}

function forgot($email){
    require ("dbConfig.php");
    
    $sql = "SELECT * FROM users where email= '$email'";
    $result = $pdo->query($sql);
    if($result->rowCount() == 1){
        echo 'Vaild Email';
    }else{
        echo "Invaild Email";
    }    
}

function resetPassword($email,$password){
    require ("dbConfig.php");
    
    $sql = "SELECT * FROM users where email= '$email'";
    $result = $pdo->query($sql);
    if($result->rowCount() == 1){
        $sql = "UPDATE `users` SET `password`='$password' WHERE email= '$email'";    
        $pdo->exec($sql);
        echo 'Updated Password';
    }else{
        echo "Failed to Updated";
    }
}

//function to launch the model
function start_model($server_link, $user_id){
    //this if for linux
    // exec('python3 ../ml-model/start_model.py "'.$server_link.'" "'.$user_id.'" > /dev/null 2>&1 &');

    //this is for windows
    exec('start "" python ..\ml-model\start_model.py "'.$server_link.'" "'.$user_id.'"');

    return "camera is starting";
}



function update_posture($user_id, $posture){
    require ("dbConfig.php");
      
    $sql = "INSERT INTO `statistics` (`user_id`, `posture`) values ($user_id,'$posture')";    
    $pdo->exec($sql);
    return "Posture added Successfully";
}

function get_statistics(){
    require ("dbConfig.php");

    session_start();
    $user_id = $_SESSION['id'];

    $sql = "SELECT * FROM `statistics` where `user_id` = '$user_id' AND `posture` = '0'";   
    $result = $pdo->query($sql);
    $all_time_wrong_posture = $result->rowCount();

    $sql = "SELECT * FROM `statistics` where `user_id` = '$user_id' AND `posture` = '1'";   
    $result = $pdo->query($sql);
    $all_time_right_posture = $result->rowCount();

    // $sql = "SELECT `posture` FROM `statistics` where `user_id` = '$user_id' AND DATE_FORMAT(`timestamp`, '%Y-%m-%d') = CURDATE() ORDER BY `timestamp` ASC";   
    // $result = $pdo->query($sql);
    // $postures = $result->fetchAll(\PDO::FETCH_NUM);

    $sql = "SELECT * FROM `statistics` where `user_id` = '$user_id' AND `posture` = '0' AND DATE_FORMAT(`timestamp`, '%Y-%m-%d') = CURDATE()";   
    $result = $pdo->query($sql);
    $todays_wrong_posture = $result->rowCount();

    $sql = "SELECT * FROM `statistics` where `user_id` = '$user_id' AND `posture` = '1' AND DATE_FORMAT(`timestamp`, '%Y-%m-%d') = CURDATE()";   
    $result = $pdo->query($sql);
    $todays_right_posture = $result->rowCount();

   

    header('Content-type: application/json');
    echo json_encode(array('allTimeRightPosture'=>$all_time_right_posture, 'allTimeWrongPosture'=>$all_time_wrong_posture, 
        'todaysRightPosture'=>$todays_right_posture, 'todaysWrongPosture'=>$todays_wrong_posture
    ));
}


unset($pdo);
?>