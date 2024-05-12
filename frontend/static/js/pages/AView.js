import { navigateTo } from '../router.js';
import { userNotification } from '../components/userNotification.js';;

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

	notify(message, type='success') {
		userNotification(message, type);
		setTimeout(() => {
			document.querySelector('.notification').remove();
		}, 3000);
	}

	updateMain(...elements) {
		const main = document.querySelector('main');
		main.innerHTML = '';
		elements.forEach((element) => {
			if (element){
				main.appendChild(element);
			}
		});
	}
}

