const body = document.querySelector('body');
const article = document.querySelector('article');
const walk = {x: 50, y: 50};

function parallax(e) {
    const width = article.offsetWidth;
    const height = article.offsetHeight;

    let { offsetX: x, offsetY: y} = e;

    const xWalk = Math.round((e.x / width / 2 * walk.x) - (walk.x / 2));
    const yWalk = Math.round((e.y / height / 2  * walk.y) - (walk.y / 2));

    article.style.transform = `rotateY(${-xWalk}deg) rotateX(${yWalk}deg)`;
}

body.addEventListener('mousemove', parallax);