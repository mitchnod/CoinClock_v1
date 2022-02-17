//starting variables
var coin = 0.00;
var minutes = 0;

function start(){
    //sets variables
    var hours = document.getElementById('hours').value;
    var pay = document.getElementById('pay').value;

    //starts counting based on pay input
    var interval = setInterval(() => {
        minutes += 1;
        coin += (pay/60);
        document.getElementById('earnings').innerText = '$ ' + coin.toFixed(2);
        //stops counting based on hour input
        if (minutes == hours * 60){
            clearInterval(interval);
            document.getElementById('earnings').style.color = "gold";
        }
    }, 60000);
}