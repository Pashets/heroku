function SeePassword() {
    const inputPass = document.getElementById("idPassword");
    if (inputPass.type === "password") {
        inputPass.type = "text";
    } else {
        inputPass.type = "password";
    }
}

function fnc() {
    alert('Еще не сделано! Ждите!');
    let email_text = document.getElementById("idEmail");
    let password_text = document.getElementById("idPassword");
}
