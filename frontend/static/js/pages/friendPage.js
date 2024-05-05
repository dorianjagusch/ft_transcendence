import AView from "./AView.js";

export default class extends AView {

	constructor(params){
		super(params);
		this.setTitle("Freeeeen");
	}

	async getHTML () {

		const leaderBoardTitle =
		'<h2>Dis yo friend?</h2>';

		const main = document.querySelector('main');
		main.innerHTML = '';
		main.appendChild(leaderBoardTitle);
	};
}