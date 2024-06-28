import Aview from './AView.js';

export default class extends Aview {
	constructor() {
		super();
		this.setTitle('Modal');
	}

	async getHTML() {
		const modal = document.createElement('div');
		modal.classList.add('modal');
	}
}
