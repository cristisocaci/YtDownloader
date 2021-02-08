function sendLink() {
    let titles = document.getElementsByName('title');
    for(let i = 0; i < titles.length; ++i){
        if(titles[i].value === ''){
            return;
        }
    }
    document.getElementById('btnsubmit').hidden=true;
    document.getElementById('btnback').hidden=true;
    document.getElementById('spinner').style.display = 'flex';
}

function update(){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200){
            if(this.responseText === 'home'){
                window.location.replace('/')
            }
            document.getElementById('base').innerHTML=this.responseText;
            let done = document.getElementById('done');
            if(done.value === 'True') {
                console.log("Done");
                stopAnimation();
                clearInterval(intervalId)
             }
        }
    };
    let identifier = document.getElementById("identifierdiv").innerText;
    xhttp.open("GET", "/fetchupdate?identifier="+identifier, true);
    xhttp.send();
}

function stopAnimation() {
    let elem = document.getElementById('animation');
    if( elem != null){
        elem.hidden = true;
    }
}
var intervalId = setInterval(function () {
    update();
},2000);