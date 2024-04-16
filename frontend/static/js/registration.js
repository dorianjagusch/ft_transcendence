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
    e.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(e.target); // Access the form using e.target
    console.log(formData);
    try {
        const response = await fetch(`${base_url}/users/`, {
            method: "POST",
            body: formData
        });
        console.log(response.data);
        // Handle the response as needed
    } catch (error) {
        console.error('Error:', error);
        // Handle errors here
    }
});

export {confirmPassword}