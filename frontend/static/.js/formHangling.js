const base_url = "127.0.0.1:8000";

const confirmPassword = function () {
    const userPassword = document.getElementById("pwd");
    const confirmPassword = document.getElementById("repeat-pwd");
    if (userPassword.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Passwords Don't Match");
    } else {
        confirmPassword.setCustomValidity("");
    }
}

const registerUser = async () => {
    const formData = new FormData(document.getElementById("registration-form"));
    console.log(formData);
    const request = await fetch(`${base_url}/users/`, {
        method: "post",
        body: formData,
    });
    return request.then(response => response.data);
}

export { confirmPassword, registerUser };
