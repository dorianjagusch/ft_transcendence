import AView from "./AView.js";

export default class extends AView {

	constructor(params){
		super(params);
		this.setTitle("Freeeeen");
	}

	async getHTML () {

		const leaderBoardTitle =
		'<h2>Dis yo friend?</h2>';

		this.updateMain(leaderBoardTitle);
	};
}