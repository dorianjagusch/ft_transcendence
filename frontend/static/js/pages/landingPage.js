import AView from "./AView.js";

export default class extends AView {

	constructor(params){
		super(params);
		this.setTitle("Landing Page");
	}

	async getHTML () {

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


		const main = document.querySelector('main');
		main.innerHTML = '';
		main.appendChild(leaderBoard);
		main.appendChild(welcomeSection);
	};
}

