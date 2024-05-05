import AView from "./AView.js";

export default class extends AView {

	constructor(){
		super();
		this.setTitle("404 Not Found");
	}

	async getHTML () {

		const leaderBoardTitle = '<h2>Page not found</h2>';
		const main = document.querySelector('main');
		main.innerHTML = '';
		main.appendChild(leaderBoardTitle);

	};
}