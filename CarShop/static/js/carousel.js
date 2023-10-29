function StartCarouselScrolling(carouselId, time, slideCondition) {
    document.addEventListener("DOMContentLoaded", function() {
        var slideNum = 0;
        var timeoutId = null;
        const slides = document.querySelectorAll(`#${carouselId} > .carousel-item`);

        if (slides.length < 1) {
            return;
        } else if (slides.length == 1) {
            slides[0].style.display = "block";
            return;
        }

        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
            slides[i].className += " passive";
            slides[i].style.marginBottom = `-${slides[0].offsetHeight}px`;
        }

        showSlides();

        function showSlides() {
            var slideIndex = slideNum % slides.length;

            if (slideCondition()) {
                for (i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                    slides[i].className = slides[i].className.replace("active", "passive")
                    slides[i].style.marginTop = "0px";
                }

                slides[slideIndex].style.display = "block";
                slides[slideIndex].className = slides[slideIndex].className.replace("passive", "active");

                if (slideNum == 0) {
                    slides[slideIndex].className = slides[slideIndex].className.replace("active", "")
                } else {
                    if (slideNum == 1) {
                        slides[0].className = slides[slideIndex].className.replace("active", "passive")
                    }

                    slides[(slideIndex + slides.length - 1) % slides.length].style.display = "block";
                    slides[slideIndex].style.marginTop = `-${slides[slideIndex].offsetHeight}px`;
                }

                if (slideIndex == 0) {
                    slides[slideIndex].style.marginTop = `0px`;

                    var prev = (slideIndex + slides.length - 1) % slides.length;
                    slides[prev].style.marginTop = `-${slides[slideIndex].offsetHeight}px`;
                }

                slideNum++;
            }

            if (timeoutId) {
                clearTimeout(timeoutId);
            }

            timeoutId = setTimeout(showSlides, time);
        }
    });
}


