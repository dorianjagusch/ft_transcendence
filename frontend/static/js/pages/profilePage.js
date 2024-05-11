import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Freeeeen');
	}

	async getHTML() {
		

		this.updateMain();
	}
}
