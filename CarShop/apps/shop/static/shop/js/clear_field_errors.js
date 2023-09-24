function clearFieldErrors(inputId) {
    var input = document.getElementById(inputId);
    input.classList.remove('is-invalid');

    var errorMessageField = input.parentElement.querySelector('span.invalid-feedback')

    while (errorMessageField.firstChild) {
        errorMessageField.removeChild(errorMessageField.firstChild);
    }
}