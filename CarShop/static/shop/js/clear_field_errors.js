function clear_field_errors(input_id) {
    var input = document.getElementById(input_id);
    input.classList.remove('is-invalid');

    var error_message_field = document.querySelector(`#${input_id} + span.invalid-feedback`)

    while (error_message_field.firstChild) {
        error_message_field.removeChild(error_message_field.firstChild);
    }
}