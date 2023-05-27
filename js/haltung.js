function logout() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText) {
                window.location.href = "index.html"
            }
        }
    };
    xhttp.open("GET", "apis/check_status.php", false);
    xhttp.send();
}

function loadData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (!this.responseText) {
                window.location.href = "index.html"
            }
        }
    };
    xhttp.open("GET", "apis/check_status.php", false);
    xhttp.send();
}

function startModel(){
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //notify user model has begun running
            // console.log(this.responseText);
        }
    };
    xhttp.open("GET", "apis/start_model.php", false);
    xhttp.send();

    //display camera is starting
    document.getElementById('model-button').innerText = 'Starting...';

    // sleep for 5 sec
    setTimeout(() => { 
        document.getElementById('model-button').innerText = 'Started'; 
        document.getElementById('model-status').innerText = 'HALTUNG Detection is Running';

    }, 5000);
    

}


function getStatistics(){
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //notify user model has begun running
            console.log(this.responseText);

            const postureRatios = new Array()
            var postures = JSON.parse(this.responseText)

            var chart = new CanvasJS.Chart("chartContainer", {
                animationEnabled: true,

                title:{
                    text: "All Time Sitting Posture"
                },
                data: [
                {
                    // Change type to "doughnut", "line", "splineArea", etc.
                    type: "pie",
                    startAngle: 240,
                    dataPoints: [
                        {y: postures.allTimeRightPosture, label: 'Right Posture'},
                        {y: postures.allTimeWrongPosture, label: 'Wrong Posture'}
                    ]
                }
                ]
            });
            chart.render();
            
            // postures.postures.forEach(element => {
            //     postureRatios.push({
            //         y: parseInt(element[0])
            //     })
            // });

            var chart2 = new CanvasJS.Chart("chartContainerDays", {
                animationEnabled: true,

                title:{
                  text: "Today's Sitting Posture"
                },
                data: [
                {
                  // Change type to "doughnut", "line", "splineArea", etc.
                  type: "doughnut",
                  dataPoints: [
                    {y: postures.todaysRightPosture, label: 'Right Posture'},
                    {y: postures.todaysWrongPosture, label: 'Wrong Posture'}
                ]
                }
                ]
              });
              chart2.render();
    

        }
    };
    xhttp.open("GET", "apis/get_statistics.php", false);
    xhttp.send();
}