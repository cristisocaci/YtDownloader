function sendLink(type) {
    if(type==='left'){
        document.getElementById('spinnerright').hidden = true;
    }
    else if(type ==='right'){
        document.getElementById('spinnerleft').hidden = true;
    }
    document.getElementById('spinner1').style.display = 'flex';
    document.getElementById('spinner2').style.display = 'flex';
    document.getElementById('btnleft').hidden=true;
    document.getElementById('btnright').hidden=true;
}

