const navbarToggler = document.querySelector(".navbar__toggler");
const navMenu = document.querySelector(".navbar__collapse");

navbarToggler.addEventListener("click", function() {
    navbarToggler.classList.toggle("active");
    navMenu.classList.toggle("active");
});

const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach(link =>
    link.addEventListener("click", function() {
        navMenu.classList.remove("active");
    })
);