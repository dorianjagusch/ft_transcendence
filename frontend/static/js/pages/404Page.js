import AView from './AView.js';

export default class extends AView {
	constructor() {
		super();
		this.setTitle('404 Not Found');
	}

	async getHTML() {
		const title404 = document.createElement('h2');
		title404.innerText = 'Page not found';

		this.updateMain(title404);
	}
}
