import AView from './AView.js';
import { GameCard } from '../components/gameCard.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Play');
	}

	async getHTML() {
		const gameOne = GameCard('Pong', 'pong-front', 'pong-card');
		const gameTwo = GameCard('Other game', 'pong-front', 'pong-card');

		this.updateMain(gameOne, gameTwo);
		const main = document.querySelector('main');
		main.classList.add('flex-row');
	}
}
