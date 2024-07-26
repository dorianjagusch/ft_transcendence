import AView from './AView.js';
import getProfilePicture from '../components/profilePicture.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileImg from '../components/profileComponents/profileImg.js';
import arrayToElementsList from '../components/profileComponents/arrayToElementsList.js';
import profileDescription from '../components/profileComponents/profileDescription.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';
import {scrollContainer} from '../components/scrollContainer.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import profileSummaryStats from '../components/profileComponents/profileSummaryStats.js';
import userData from '../userAPIData/userAPIDashboard.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Dashboard');
	}

	async getHTML() {
		if (localStorage.getItem('isLoggedIn') === 'false') {
			this.navigateTo('/login');
			return;
		}

		const title = profileTitle('Your Stats');

		let profileImage;
		try {
			profileImage = profileImg(await getProfilePicture(localStorage.getItem('user_id')));
		} catch (error) {
			notify(error, 'error');
		}

		const userPlacement = arrayToElementsList(
			userData.placements,
			'placements',
			smallPlacementCard
		);
		userPlacement.classList.add('flex-col');
		const userDescription = profileDescription(userData.user.description);

		const userHistory = scrollContainer(userData.playHistory, profilePlayHistory, 'column');
		userHistory.classList.add('play-history');

		const userSummary = profileSummaryStats(userData.stats);

		const main = document.querySelector('main');
		main.classList.add('profile', 'dashboard');
		this.updateMain(
			title,
			profileImage,
			userPlacement,
			userDescription,
			userSummary,
			userHistory
		);
	}
}
