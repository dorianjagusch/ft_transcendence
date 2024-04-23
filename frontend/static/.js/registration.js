const confirmPassword = function() {
    const userPassword = document.getElementById("pwd");
    const confirmPassword = document.getElementById("repeat-pwd");
    if (userPassword.value !== confirmPassword.value){
        confirmPassword.setCustomValidity("Passwords Don't Match");
    } else {
        confirmPassword.setCustomValidity("");
    }
}

const base_url = "http://127.0.0.1:8000";


document.getElementById("registration-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    console.log(formData);
    try {
        const response = await fetch(`${base_url}/users/`, {
            method: "POST",
            body: formData
        });
        console.log(response.data);
    } catch (error) {
        console.error('Error:', error);
    }
});

export {confirmPassword}