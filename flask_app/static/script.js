//starting variables
var coin = 0.00;
var minutes = 0;
var seconds = 0;

function start(){
    //sets variables
    var hours = document.getElementById('hours').value;
    var pay = document.getElementById('pay').value;

    //starts counting based on pay input
    var interval = setInterval(() => {
        seconds += 1;
        console.log(seconds)
        coin += (pay/3600);
        document.getElementById('earnings').innerText = '$ ' + coin.toFixed(2);
        //stops counting based on hour input
        if (seconds%60 == 0){
            minutes += 1;
            console.log(minutes)
        }
        if (minutes == hours * 60){
            clearInterval(interval);
            document.getElementById('earnings').style.color = "gold";
        }
    }, 1000);
}