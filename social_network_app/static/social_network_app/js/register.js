let username = document.getElementById("id_username")
username.classList.add('form-control')
username.placeholder = "Username"
let password1 = document.getElementById("id_password1")
password1.classList.add('form-control')
password1.placeholder = "Password"
let password2 = document.getElementById("id_password2")
password2.classList.add('form-control')
password2.placeholder = "Confirm password"

let password_rules = '<br>Your password can\'t be too similar to your other personal information.<br>Your password must contain at least 8 characters.<br>Your password can\'t be a commonly used password.<br>Your password can\'t be entirely numeric.'

function insertAfter(el, referenceNode) {
    referenceNode.parentNode.insertBefore(el, referenceNode.nextSibling);
}

let rules = document.createElement('div');
rules.classList.add('alert')
rules.classList.add('alert-info')
rules.classList.add('mt-3')
rules.innerHTML = `<p>${password_rules}</p>`;
insertAfter(rules, password1);