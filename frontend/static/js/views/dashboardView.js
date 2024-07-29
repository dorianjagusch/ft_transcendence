import AView from './AView.js';
import MatchService from '../services/matchService.js';
import PlayerService from '../services/playerService.js';
import LeaderboardService from '../services/leaderboardService.js';
import StatsService from '../services/statsService.js';
import UserService from '../services/userService.js';
import getProfilePicture from '../components/profilePicture.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileImg from '../components/profileComponents/profileImg.js';
import {scrollContainer} from '../components/scrollContainer.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import profileSummaryStats from '../components/profileComponents/profileSummaryStats.js';
import constants from '../constants.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Dashboard');
		this.matchService = new MatchService();
		this.playerService = new PlayerService();
		this.leaderBoardService = new LeaderboardService();
		this.statsService = new StatsService();
		this.userService = new UserService();
		this.userId = localStorage.getItem('user_id');
	}

	async getOpponent(players) {
		let opponent = players.find((player) => player.user != this.userId);
		if (!opponent) {
			opponent = {};
			opponent.username = 'AI';
		} else {
			try {
				const opponentData = await this.userService.getRequest(opponent.user);
				opponent.username = opponentData.username;
			} catch (error) {
				opponent.username = 'Deleted User';
			}
		}
		return opponent;
	}

	async getFinishedMatches() {
		const allMatches = await this.matchService.getHistoryMatches(this.userId);
		const finishedMatches = allMatches.filter(
			(match) => match.state === constants.MATCHSTATUS.FINISHED
		);
		debugger;
		const matchData = await Promise.all(
			finishedMatches.map(async (match) => {
				const players = await this.matchService.getMatchPlayers(match.id);
				const opponent = await this.getOpponent(players);
				const self = players.find((player) => player.user == this.userId);
				return {
					match_id: match.id,
					opponent: opponent.username,
					opponentId: opponent.id ?? 'AI',
					winner: self.score > opponent.score,
					scoreSelf: self.score,
					scoreOpponent: opponent.score,
					date: match.insert_ts,
				};
			})
		);
		return matchData;
	}

	async getHTML() {
		if (localStorage.getItem('isLoggedIn') === 'false') {
			this.navigateTo('/login');
			return;
		}

		const title = profileTitle('Your Stats');

		let profileImage;
		let stats;
		let history;
		let winLossGraph;
		let recentOutcomesGraph;
		try {
			profileImage = profileImg(await getProfilePicture(this.userId));
			stats = await this.statsService.getRequest(this.userId);
			history = await this.getFinishedMatches();
		} catch (error) {
			this.notify(error, 'error');
			return;
		}
		try {
			winLossGraph = await this.statsService.getImage(this.userId, 'win-loss');
			recentOutcomesGraph = await this.statsService.getImage(this.userId, 'recent-outcomes');
		} catch (error) {
			this.notify(error, 'error');
			return;
		}

		const userHistory = scrollContainer(history, profilePlayHistory, 'col');
		userHistory.classList.add('play-history', 'bg-secondary');
		const header = document.createElement('h2');
		header.textContent = 'History';
		userHistory.insertBefore(header, userHistory.firstChild);

		const userSummary = profileSummaryStats(stats);

		const stats1 = document.createElement('section');
		stats1.innerHTML = winLossGraph;
		console.log(stats1);
		stats1.classList.add('play-graph', 'play-graph-1');

		const stats2 = document.createElement('section');
		stats2.innerHTML = recentOutcomesGraph;
		stats2.classList.add('play-graph', 'play-graph-2');

		const main = document.querySelector('main');
		main.classList.add('profile', 'dashboard');
		this.updateMain(title, profileImage, userSummary, userHistory, stats1, stats2);
	}
}
