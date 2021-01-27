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
