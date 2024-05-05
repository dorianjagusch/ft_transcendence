import AView from "./AView.js";

const showLandingPage = () => {
  const main = document.querySelector("main");
  main.innerHTML = "";

  const loginButton = document.querySelector("#login");
  loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    stateMachine.transition("goToLogin");
  });

  const registerButton = document.querySelector("#register");
  registerButton.addEventListener("click", (e) => {
    e.preventDefault();
    stateMachine.transition("goToRegister");
  });

  const leaderBoard = document.createElement("section");
  leaderBoard.classList.add("bg-secondary");
  const leaderBoardTitle =
    '<h2>Leaderboard</h2><ul class="col-scroll placements"></ul></section>';
  leaderBoard.innerHTML = leaderBoardTitle;
  // fillLeaderBoard();  TODO: Uncomment this line when the backend is ready

  const welcomeSection = document.createElement("section");
  welcomeSection.setAttribute("id", "welcome");
  const welcomeHtml = "<h2>Welcome</h2><h3>to the great pong tournament</h3>";
  welcomeSection.innerHTML = welcomeHtml;

  main.appendChild(leaderBoard);
  main.appendChild(welcomeSection);
};

export default showLandingPage;
