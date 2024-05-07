import { navigateTo } from '../router.js';

export default class {
	constructor(params) {
		this.params = params;
	}

	setTitle(title) {
		document.title = title;
	}

	navigateTo(path) {
		navigateTo(path);
	}

	async getHTML() {
		return;
	}

	updateMain(...elements) {
		const main = document.querySelector('main');
		main.innerHTML = '';
		elements.forEach((element) => {
			main.appendChild(element);
		});
	}
}
