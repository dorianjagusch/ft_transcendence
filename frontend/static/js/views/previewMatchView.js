import Aview from './AView.js';
import {PlayerInfo} from '../components/playerInfo.js';
import UserService from '../services/userService.js'; // TODO: Switch out for stats service
import getProfilePicture from '../components/profilePicture.js';
import constants from '../constants.js';
import TournamentService from '../services/tournamentService.js';

export default class extends Aview {
	constructor(params) {
		super(params);
		this.setTitle('Modal');
		this.userService = new UserService();
		this.tournamentService = new TournamentService();
		this.attachEventListeners = this.attachEventListeners.bind(this);
	}

	attachEventListeners() {
		const startButton = document.querySelector('.start-btn');
		if (startButton) {
			startButton.addEventListener('click', () => {
				this.navigateTo(
					`/pong/tournaments/${this.params.tournament_id}/matches/${this.params.match_id}`
				);
			});
		}
	}

	continueButton() {
		const container = document.createElement('div');
		const vs = document.createElement('h2');
		vs.classList.add('vs');
		vs.textContent = 'vs';
		const startButton = document.createElement('button');
		startButton.classList.add('accept-btn', 'start-btn');
		startButton.textContent = 'Start Game';
		container.appendChild(vs);
		container.appendChild(startButton);
		return container;
	}

	async setupPlayerInfo(userId) {
		const userData = await this.userService.getRequest(userId); // REQUEST TO /user/stats
		userData.img = await getProfilePicture(userId);
		const player = PlayerInfo(userData);
		return player;
	}

	async getCurrentMatchData() {
		const matchData = await this.tournamentService.getTournamentMatches(this.params);
		return matchData.find(
			(match) =>{
				return match.state === constants.MATCHSTATUS.LOBBY
			}
		);
	}

	async getHTML() {
		let playerLeft = null;
		let playerRight = null;
		let matchData = null;
		// TODO: Add stats to userService
		try {
			matchData = await this.getCurrentMatchData();
			if (!matchData) {
				return '<h1>No match data found</h1>';
			}
			playerLeft = await this.setupPlayerInfo(matchData.tournament_player_left.user);
			console.log(playerLeft);
			playerRight = await this.setupPlayerInfo(matchData.tournament_player_right.user);
		} catch (error) {
			console.log(error);
		}

		const continueButton = this.continueButton();

		const main = document.querySelector('main');
		main.classList.add('flex-row');

		super.updateMain(playerLeft, continueButton, playerRight);
		this.attachEventListeners();
	}
}
