import AView from './AView.js';
import { GameCard } from '../components/gameCard.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Play');
	}

	attachEventListeners() {
		const gameCard = document.querySelector('.game-card');
		gameCard.addEventListener('click', () => {
			this.navigateTo('/match');
		});
	}

	async getHTML() {
		const gameOne = GameCard('Pong', 'pong-front', 'pong-card');
		this.updateMain(gameOne);
		const main = document.querySelector('main');
		main.classList.add('flex-row');
		this.attachEventListeners();
	}
}
