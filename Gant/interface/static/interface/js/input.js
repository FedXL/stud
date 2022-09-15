const buttonElem = document.getElementById('sub_button');

let onButtonClick = function () {
    let x = 3
    const details = document.getElementById('detail').value;
    const tools = document.getElementById('stanki').value;
    const series = document.getElementById('batch').value;
    const sum = details*tools*series
    if (sum >= 1250){
        alert(`ВАМ точно нужно так МНОГО?
        для целей изучения хватит 10 деталей и 10 станков.
        при большем сете моя неоптимизированная программа будет долго всё считать,
        а при сете больше 25х25 скорее всего умрёт,но это не точно, на финальной стадии отрисовке диаграмм
        ганта.`)
    }
}

buttonElem.addEventListener('click',onButtonClick);