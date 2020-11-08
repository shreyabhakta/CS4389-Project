//test function (remove later)
function myOnClickFn() {
    document.location.href = "bankUser.html";
}

function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");

    document.querySelector("#linkCreateAccount").addEventListener("click", e => {
        e.preventDefault();
        loginForm.classList.add("form--hidden");
        createAccountForm.classList.remove("form--hidden");
    });

    document.querySelector("#linkLogin").addEventListener("click", e => {
        e.preventDefault();
        loginForm.classList.remove("form--hidden");
        createAccountForm.classList.add("form--hidden");
    });

    createAccountForm.addEventListener("submit", (e) => {
        e.preventDefault();

        console.log(createAccountForm);

        // Password do not match
        if (document.getElementById("create_password").value != document.getElementById("create_password_confirm").value) {
            alert('password dont match!');
        }

        fetch('/createaccount', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            redirect: "follow",
            body: JSON.stringify({
                "email": document.getElementById("create_email").value,
                "password": document.getElementById("create_password").value,
                "first": document.getElementById("create_first").value,
                "last": document.getElementById("create_last").value,
                "phone": document.getElementById("create_phone").value,
                "ssn": document.getElementById("create_ssn").value,
            })
        }).then(response => {
            if (response.redirected) {
                console.log("redirected");
                window.location.href = response.url;
            }
            else {
                (async () => {
                    data = await response.text()
                    // Notify the user of the cause
                    alert(data);
                })()
            }
            console.log(response);
        });

        // POST request to create an account
    })

    loginForm.addEventListener("submit", e => {
        e.preventDefault();
        console.log("Called")
        // Perform your AJAX/Fetch login

        // Should Do this for wider support 
        // But not done since can't handle redirect request
        // var xhr = new XMLHttpRequest();
        // xhr.open("POST", "login", true);
        // xhr.setRequestHeader('Content-Type', 'application/json');
        // xhr.send(JSON.stringify({
        //     "value": "value",
        //     "email": "email"
        // }));

        // TODO: Check and cleanse the input

        // Not Compatible with all browsers/ Specifically Old IE's

        console.log(JSON.stringify(loginForm));

        fetch('/login', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            redirect: "follow",
            body: JSON.stringify({
                "email": document.getElementById("login_email").value,
                "password": document.getElementById("login_password").value
            })
        }).then(response => {
            if (response.redirected) {
                console.log("redirected");
                window.location.href = response.url;
            }
            else {
                (async () => {
                    data = await response.text()
                    // Notify the user of the cause
                    alert(data);
                })()
            }
        });

    });
});