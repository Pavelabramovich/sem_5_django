function clearFieldErrors(input_id) {
    var input = document.getElementById(input_id);
    input.classList.remove('is-invalid');

    var errorMessageField = input.parentElement.querySelector('span.invalid-feedback')

    while (errorMessageField.firstChild) {
        errorMessageField.removeChild(errorMessageField.firstChild);
    }
}