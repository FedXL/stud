const first = document.documentElement;
const hea = document.head;
const bo = document.getElementById('super_table');

console.log(bo);

console.log(bo.firstChild);
console.log(bo.lastChild);
console.log(bo.childNodes);


console.log(bo.previousSibling);
console.log(bo.nextSibling);
console.log(bo.parentNode);

console.log('childnodes',bo.childNodes);
console.log('children',bo.children);

console.log('firstElementChild',bo.firstChild);
console.log('lastElementChild' ,bo.lastChild);

const first = document.documentElement;
const hea = document.head;
const bo = document.getElementById('super_table');

const table_body = first.childNodes[2].childNodes[3].childNodes[5].childNodes[3].innerHTML;
console.log(table_body);
var str ='<tr><td> detail - хх </td><td><input value={350}/></td><td><input value={400}/></td><td><button>del</button></td></tr>' ;


var doo = document.querySelectorAll('.super>tbody>tr');
console.log(doo);

var lifedo = document.getElementsByTagName('tr');
console.log(lifedo[1].innerHTML);

