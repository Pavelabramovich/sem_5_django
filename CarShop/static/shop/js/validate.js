function validate(input_id) {
    var input = document.getElementById(input_id);
    var string = input.value

    if (string.length > 5) {
        throw { name: 'ValidationError', message: 'Data is invalid!!!' };
    }
}