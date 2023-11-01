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
    var string = input.value;

    var result = string.match(phone_re);

    if (result === null) {
        throw { name: 'ValidationError', message: 'Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.' };
    }
}

var address_re = /^((\b([A-Za-z]+)\b)|(\b([\d\.\-]+)\b)|([\s,\.\:\!]*))*$/;

function validateAddress(inputId) {
    var input = document.getElementById(inputId);
    var string = input.value;

    var result = string.match(address_re);

    if (result === null) {
        throw { name: 'ValidationError', message: 'Address is incorrect. It must consist of words, numbers and codes.' };
    }
}


function validateBirthday(inputId) {

    var input = document.getElementById(inputId);

    var birthday = input.value;
    birthday = new Date(birthday);


    var today = new Date();

    var ageInSeconds = today - birthday;

    const secondsInYear = 1000 * 60 * 60 * 24 * 365.25

    if (ageInSeconds < 18 * secondsInYear) {
        throw { name: 'ValidationError', message: 'You must be at least 18 years old.' };
    } else {
        const age = Math.floor(ageInSeconds / secondsInYear);
        const weekDay = birthday.toLocaleString('en-us', {weekday:'long'})

        alert(`Your age is ${age}, day of week your birthday is ${weekDay}`)
    }
}
