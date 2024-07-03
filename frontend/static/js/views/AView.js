import {navigateTo} from '../router.js';
import {userNotification} from '../components/userNotification.js';
import {Navbar} from '../components/navbar.js';
import SideBar from '../components/sideBar.js';

export default class Aview{
	constructor(params) {
		this.params = params;
		if (this.constructor == Aview) {
			throw new Error("Abstract classes can't be instantiated.");
		}
		if (!document.querySelector('nav')) {
			document.querySelector('header').appendChild(Navbar());
		}
		if (!document.querySelector('aside') && localStorage.getItem('isLoggedIn') === 'true') {
			document.querySelector('body').appendChild(SideBar());
		}
	}

	setTitle(title) {
		document.title = title;
	}

	navigateTo(path) {
		navigateTo(path);
	}

	getHTML() {
		return;
	}

	notify(message, type = 'success') {
		userNotification(message, type);
		setTimeout(() => {
			document.querySelector('.notification').innerText = '';
		}, 3000);
	}

	updateMain(...elements) {
		const main = document.querySelector('main');
		main.innerHTML = '';
		elements.forEach((element) => {
			if (element) {
				main.appendChild(element);
			}
		});
	}
}
