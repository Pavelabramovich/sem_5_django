const truckLeft = document.querySelector('#truck_left');
const truckRight = document.querySelector('#truck_right');

window.addEventListener('scroll',() => {
    truckLeft.style.left = `${truckLeft.clientWidth}px`;
    truckRight.style.left = `-${truckRight.clientWidth}px`;

    truckLeft.style.top = `${truckLeft.clientHeight / 2}px`;
    truckRight.style.top = `-${truckRight.clientHeight / 2 + 5}px`;

    var rect = truckLeft.getBoundingClientRect();

    var value = rect.top + truckLeft.clientHeight * 2.7;
    var offset = Math.min(truckLeft.clientWidth - (value * 1.85), -window.innerWidth / 2 + 10)

    truckLeft.style.left = `${offset}px`;
    truckRight.style.left = `${-offset}px`;
})




