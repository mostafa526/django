var input = document.querySelector('.newPasswordReset');
var error = document.querySelector('.TextError');
var timeout = null;

var showError = message => {
    error.style.color = '#C91E1E';
    error.style.display = 'block';
    error.innerHTML = message;
}

var showPass = message => {
    error.style.color = '#119822';
    error.innerHTML = message;
}

var validatePassword = password => {
    var lowerCaseRagex = new RegExp('^(?=.*[a-z])');
    var upperCaseRagex = new RegExp('^(?=.*[a-z])');
    var specialCharacterRagex = new RegExp('^(?=.*[!@#$%^&*])');
    var numericRagex = new RegExp('^(?=.*[0-9])');

    if (!password == 0) {
        if (password.length < 8) {
            showError('Your password must be at least 8 characters long.');
        } else if (!lowerCaseRagex.test(password)) {
            showError('Recommendation : Your password should include at least one lowercase character.')
        } else if (!upperCaseRagex.test(password)) {
            showError('Recommendation : Your password should include at least one uppercase character.')
        } else if (!specialCharacterRagex.test(password)) {
            showError('Recommendation : Your password should include at least one spacial character.')
        } else if (!numericRagex.test(password)) {
            showError('Recommendation : Your password should include at least one number.')
        } else {
            showPass('Strong Password!')
        }
    } else {
        showError('');
        showPass('');
    }


}

input.addEventListener('keyup', e => {
    var password = e.target.value;
    validatePassword(password);
});


var passwordMatchMessage = document.querySelector('.TextError');

$('.newPasswordResetRepeat, .newPasswordReset').on('keyup', function () {
    if ($('.newPasswordReset').val() == $('.newPasswordResetRepeat').val()) {
        $('.TextErrorMatch').html('Matching').css('color', 'green');
    } else
        $('.TextErrorMatch').html('Not Matching').css('color', 'red');
});

document.getElementById("Button").disabled = true;

$('.newPasswordResetRepeat, .newPasswordReset').on('keyup', function () {

    if (($('.newPasswordReset').val() == $('.newPasswordResetRepeat').val()) && (input.value.length >= 8)) {
        document.getElementById("Button").disabled = false;
    } else {
        document.getElementById("Button").disabled = true;
    }


});
