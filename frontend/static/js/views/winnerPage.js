import AView from './AView.js';
import {PlayerInfo} from '../components/playerInfo.js';
import TournamentService from '../services/tournamentService.js';
import MatchService from '../services/matchService.js';
import PlayerService from '../services/playerService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Tournament Winner');
		this.tournamentService = new TournamentService();
		this.matchService = new MatchService();
		this.PlayerService = new PlayerService();
	}

	async getHTML() {
		if (this.params.tournament_id) {
			try {
				const tournamentData = await this.tournamentService.getTournamentMatches(this.context);
				const winner = tournamentData[tournamentData.length - 1].winner;
				debugger
				winner.img = await getProfilePicture(winner.id);
				console.log(winner);
			} catch (error) {
				this.notify(error.message);
			}
		} else {
			this.matchService()
		}
		const congratsElement = document.createElement('h2');
		congratsElement.textContent = 'Congratulations!';
		const winnerInfo = PlayerInfo(winner);
		winnerInfo.classList.add('winner');
		const winnerDeclaration = document.createElement('h3');
		winnerDeclaration.textContent = `${winner.display_name} is the winner!`;
		document.querySelector('main').classList.add('flex-col');
		this.updateMain(congratsElement,winnerInfo, winnerDeclaration);
	}
}
