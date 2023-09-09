function validatePasswordConfirmation(password1Id, password2Id) {
    var password1 = document.getElementById(password1Id)
    var password2 = document.getElementById(password2Id)

    if (password1.value !== password2.value) {
        throw { name: 'ValidationError', message: 'The two password fields didn’t match.' };
    }
}

var phone_re = /^\+375\s*\(\s*29\s*\)\s*(\d{3})\s*-\s*(\d{2})\s*-\s*(\d{2})$/;

function validatePhone(inputId) {
    var input = document.getElementById(inputId);
    var string = input.value

    var result = string.match(phone_re);

    if (result === null) {
        throw { name: 'ValidationError', message: 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.' };
    }
}

var address_re = /^((\b([A-Za-z]+)\b)|(\b([\d\.\-]+)\b)|([\s,\.\:\!]*))*$/;

function validateAddress(inputId) {
    var input = document.getElementById(inputId);
    var string = input.value

    var result = string.match(address_re);

    if (result === null) {
        throw { name: 'ValidationError', message: 'Address is incorrect. It must consist of words, numbers and codes.' };
    }
}
