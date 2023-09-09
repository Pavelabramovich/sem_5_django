function passwordShowHide(passwordId, showPasswordId, hidePasswordId) {
    var input = document.getElementById(passwordId);

    var showPassword = document.getElementById(showPasswordId);
    var hidePassword = document.getElementById(hidePasswordId);

    if (input.type === "password") {
        input.type = "text";

        showPassword.classList.add("d-none");
        hidePassword.classList.remove("d-none");

    } else {
        input.type = "password";

        showPassword.classList.remove("d-none");
        hidePassword.classList.add("d-none");
    }
}