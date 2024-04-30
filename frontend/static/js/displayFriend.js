const friendButtons = document.querySelectorAll(".user-card")

friendButtons.forEach(userCard => {
    userCard.addEventListener("click", () => {

        const userCardText = userCard.querySelector(".user-card-text");
        const userName = userCardText.querySelector(".user-name").textContent;
        const status = userCardText.querySelector(".status").getAttribute("data-status");

        console.log("User Name:", userName);
        console.log("Status:", status);
    });
});
