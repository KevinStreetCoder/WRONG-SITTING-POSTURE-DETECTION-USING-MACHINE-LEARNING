var myInput = document.getElementById("password");
var letter = document.getElementById("letter");
var letter2 = document.getElementById("letter2");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
var cpassword = document.getElementById("cpassword");
var username = document.getElementById("username");
var email = document.getElementById("email");
var pattren = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
var pass = /^[A-Za-z]\w{7,14}$/;

// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
    document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function() {
    document.getElementById("message").style.display = "none";
}

// When the user clicks on the email field, show the message box
email.onfocus = function() {
    document.getElementById("message2").style.display = "block";
}

// When the user clicks outside of the email field, hide the message box
email.onblur = function() {
    document.getElementById("message2").style.display = "none";
}

email.onkeyup = function() {
    if (email.value.match(pattren)) {
        letter2.classList.remove("invalid");
        letter2.classList.add("valid");
    } else {
        letter2.classList.remove("valid");
        letter2.classList.add("invalid");
    }
}

// When the user starts to type something inside the password field
myInput.onkeyup = function() {
    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if (myInput.value.match(lowerCaseLetters)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
    } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if (myInput.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if (myInput.value.match(numbers)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
    }

    // Validate length
    if (myInput.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
    }
}


function check_status() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText) {
                window.location.href = "home.html"
            }
        }
    };
    xhttp.open("GET", "apis/check_status.php", false);
    xhttp.send();
}

function register() {
    var username = document.getElementsByName("username")[0].value;
    var email = document.getElementsByName("email")[0].value;
    var password = document.getElementsByName("password")[0].value;
    var cpassword = document.getElementsByName("cpassword")[0].value;
    if (username != "" && email != "" && email.match(pattren) && password != "") {
        if (cpassword != password) {
            alert("Passwords don't match");
        } else {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    alert(this.response);
                    window.location.reload()
                }
            };
            xhttp.open("POST", "apis/registration.php", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("username=" + username + "&email=" + email + "&password=" + password);
        }
    } else {
        alert("Please fill all fields");
    }
}

function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementsByName("password")[0].value;
    if (username != "" && password != "") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                alert(this.response);
                if (this.response == "Successfully Logged In") {
                    window.location.href = "home.html"
                }
            }
        };
        xhttp.open("POST", "apis/login.php", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("email=" + username + "&password=" + password);
    } else {
        alert("Please fill all fields");
    }
}

function forgot() {
    var email = document.getElementById("email").value;
    if (email != "") {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                alert(this.response);
                if (this.response == "Vaild Email") {
                    window.location.href = "resetpassword.html?email=" + email
                }
            }
        };
        xhttp.open("POST", "apis/forgot.php", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("email=" + email);
    } else {
        alert("Please fill email id");
    }
}

function resetPassword() {
    var url_string = window.location.href.split('=');
    var email = url_string[1]
    var password = document.getElementById("password").value;
    var cpassword = document.getElementById("cpassword").value;
    if (email != "") {
        if (password == "") {
            alert("Please enter password");
        } else if (cpassword != password) {
            alert("Password is not matching");
        } else {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    alert(this.response);
                    if (this.response == "Updated Password") {
                        window.location.href = "index.html"
                    }
                }
            };
            xhttp.open("POST", "apis/reset.php", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("email=" + email + "&password=" + password);
        }
    } else {
        alert("Invalid URL");
    }
}