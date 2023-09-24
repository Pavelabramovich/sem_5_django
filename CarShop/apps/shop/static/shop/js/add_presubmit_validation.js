function addPresubmitValidation() {
    'use strict'
    const forms = document.querySelectorAll('.requires-validation')

    Array.from(forms).forEach(form => {
        const useCapture = false

        var fields = Array.from(form.elements);

        form.addEventListener('submit', event => {
            var isValid = true

            fields.forEach(field => {
                var errorMessage = ''

                if ('validator' in field.dataset) {
                    try {
                        eval(field.dataset.validator)
                    } catch (error) {
                        if (error.name === 'ValidationError') {
                            errorMessage = error.message
                        }
                        else {
                            throw error
                        }
                    }
                }

                var defaultValid = field.checkValidity()

                if (!errorMessage && defaultValid) {
                    field.classList.remove('is-invalid');

                } else {
                    if (!defaultValid) {
                        if ('errorMessage' in field.dataset) {
                            errorMessage = field.dataset.errorMessage
                        } else {
                            errorMessage = "This field is required."
                        }
                    }

                    if (field.id !== '') {
                        var errorMessageField = field.parentElement.querySelector('span.invalid-feedback')

                        if (errorMessageField !== null) {
                            while (errorMessageField.firstChild) {
                                errorMessageField.removeChild(errorMessageField.firstChild);
                            }

                            var errorNode = document.createTextNode(errorMessage);
                            errorMessageField.appendChild(errorNode)
                        }
                    }
                    field.classList.add('is-invalid');
                    isValid = false
                }
            });

            if (!isValid) {
                event.preventDefault()
                event.stopPropagation()
            }
        }, useCapture)
    })
}