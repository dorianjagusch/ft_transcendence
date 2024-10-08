import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Landing Page');
	}

	getHTML() {
		const welcomeSection = document.createElement('section');
		welcomeSection.setAttribute('id', 'welcome');
		const welcomeTitle = document.createElement('h2');
		welcomeTitle.textContent = 'Welcome';
		const welcomeSubtext = document.createElement('h3');
		welcomeSubtext.textContent = 'to the great pong tournament';
		welcomeSection.appendChild(welcomeTitle);
		welcomeSection.appendChild(welcomeSubtext);

		this.updateMain(welcomeSection);
	}
}
