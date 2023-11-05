function foo(seconds, timerId) {
    function startTimer(duration, display) {
        var timer = duration;
        var minutes;
        var seconds;

        setInterval(function () {
            minutes = parseInt(timer / 60, 10)
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                timer = 0;
            }
        }, 1000);
    }

    var time = seconds;

    var display = document.querySelector(`#${timerId}`);
    startTimer(time, display);
}