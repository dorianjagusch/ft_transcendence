import AView from './AView.js';
import {PlayerInfo} from '../components/playerInfo.js';
import TournamentService from '../services/tournamentService.js';
import getProfilePicture from '../components/profilePicture.js';
import StatsService from '../services/statsService.js';
import MatchService from '../services/matchService.js';
import UserService from '../services/userService.js';
// import PlayerService from '../services/playerService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Tournament Winner');
		this.tournamentService = new TournamentService();
		this.statsService = new StatsService();
		this.matchService = new MatchService();
		this.userService = new UserService();
		// this.PlayerService = new PlayerService();
	}

	async getHTML() {
		let winner;
		if (this.params.tournament_id) {
			try {
				debugger;
				const tournamentData = await this.tournamentService.getTournamentMatches(
					this.params
				);
				winner = tournamentData[tournamentData.length - 1]?.winner;
				winner.img = await getProfilePicture(winner.user);
				winner.stats = await this.statsService.getRequest(winner.user);
				winner.username = winner.username;
			} catch (error) {
				this.notify(error.message);
			}
		} else {
			const players = await this.matchService.getMatchPlayers(this.params.match_id);
			const winnerPlayer = players.find((player) => player.match_winner);
			if (!winnerPlayer) {
				winner = {};
				this.aiflag = true;
			} else {
				const user = await this.userService.getRequest(winnerPlayer.user);
				winner = {};
				winner.username = user.username;
				winner.img = await getProfilePicture(winnerPlayer.user);
				winner.stats = await this.statsService.getRequest(winnerPlayer.user);
			}
		}
		if (this.aiflag) {
			const appologiesElement = document.createElement('h2');
			appologiesElement.textContent = 'Better luck next time!';
			this.updateMain(appologiesElement);
			return;
		}
		const congratsElement = document.createElement('h2');
		congratsElement.textContent = 'Congratulations!';
		const winnerInfo = PlayerInfo(winner);
		winnerInfo.classList.add('winner');
		const winnerDeclaration = document.createElement('h3');
		winnerDeclaration.textContent = `${winner.display_name ?? winner.username} is the winner!`;
		document.querySelector('main').classList.add('flex-col');
		this.updateMain(congratsElement, winnerInfo, winnerDeclaration);
	}
}
