

function addRows(){
    var lifedo = document.getElementsByTagName('tbody');
    var tor = lifedo[0].innerHTML
    var str =`<tr><td> detail - хх </td><td><input value=${350}></td><td><input value=${400}></td><td><button>del</button></td></tr>` ;
    lifedo[0].innerHTML = tor + str;
}

