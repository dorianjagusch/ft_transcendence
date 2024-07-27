import AView from './AView.js';
import MatchService from '../services/matchService.js';
import PlayerService from '../services/playerService.js';
import LeaderboardService from '../services/leaderboardService.js';
import getProfilePicture from '../components/profilePicture.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileImg from '../components/profileComponents/profileImg.js';
import {scrollContainer} from '../components/scrollContainer.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import profileSummaryStats from '../components/profileComponents/profileSummaryStats.js';
import userData from '../userAPIData/userAPIDashboard.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Dashboard');
		this.matchService = new MatchService();
		this.PlayerService = new PlayerService();
		this.leaderBoardService = new LeaderboardService();
	}

	async getHTML() {
		if (localStorage.getItem('isLoggedIn') === 'false') {
			this.navigateTo('/login');
			return;
		}

		const title = profileTitle('Your Stats');

		let profileImage;
		let placement;
		try {
			placement = await this.leaderBoardService.getRequest()
			profileImage = profileImg(await getProfilePicture(localStorage.getItem('user_id')));
		} catch (error) {
			notify(error, 'error');
		}

		const userHistory = scrollContainer(userData.playHistory, profilePlayHistory, 'column');
		userHistory.classList.add('play-history');

		const userSummary = profileSummaryStats(userData.stats);

		const main = document.querySelector('main');
		main.classList.add('profile', 'dashboard');
		this.updateMain(
			title,
			profileImage,
			userSummary,
			userHistory
		);
	}
}
