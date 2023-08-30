function password_show_hide(password_id, show_password_id, hide_password_id) {
    var input = document.getElementById(password_id);

    var show_password = document.getElementById(show_password_id);
    var hide_password = document.getElementById(hide_password_id);

    if (input.type === "password") {
        input.type = "text";

        show_password.classList.add("d-none");
        hide_password.classList.remove("d-none");

    } else {
        input.type = "password";

        show_password.classList.remove("d-none");
        hide_password.classList.add("d-none");
    }
}