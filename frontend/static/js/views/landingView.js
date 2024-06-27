import AView from './AView.js';
import {scrollContainer} from '../components/scrollContainer.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Landing Page');
	}

	async getHTML() {
		const welcomeSection = document.createElement('section');
		welcomeSection.setAttribute('id', 'welcome');
		const welcomeTitle = document.createElement('h2');
		welcomeTitle.textContent = 'Welcome';
		const welcomeSubtext = document.createElement('h3');
		welcomeSubtext.textContent = 'to the great pong tournament';

		const leaderBoardTitle = document.createElement('h2');
		leaderBoardTitle.textContent = 'Leaderboard';

		const leaderBoardScroller = scrollContainer(null, smallPlacementCard, 'leaderboard');
		leaderBoard.appendChild(leaderBoardScroller);

		const pongButton = document.createElement('button');
		pongButton.textContent = 'Play Pong';
		pongButton.addEventListener('click', () => {
			this.navigateTo('/pong');
		});

		this.updateMain(leaderBoard, welcomeSection, pongButton);
	}
}
