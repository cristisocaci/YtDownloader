
function update(){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200){
            document.getElementById('base').innerHTML=this.responseText;
            let done = document.getElementById('done');
            if(done.innerText === 'True') {
                console.log("Done");
                clearInterval(intervalId)
             }
        }
    };
    let identifier = document.getElementById("identifierdiv").innerText;
    xhttp.open("GET", "/downloadupdate?identifier="+identifier, true);
    xhttp.send();
}

var intervalId = setInterval(function () {
    update();
},1000);