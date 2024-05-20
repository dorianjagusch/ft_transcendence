import AView from './AView.js';
import arrayToElementsList from '../components/profileComponents/arrayToElementsList.js';
import buttonBar from '../components/profileComponents/buttonBar.js';
import profileImg from '../components/profileComponents/profileImg.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileDescription from '../components/profileComponents/profileDescription.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import profileStats from '../components/profileComponents/profileStats.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import { scrollContainer } from '../components/scrollContainer.js';


export default class extends AView {
	constructor(params) {
		super(params);
	}

	selectButtons(relationship) {
		switch (relationship) {
			case 'friend':
				return null;
			case 'not-friend':
				return [{className: 'accept-btn', textContent: 'Add Friend'}];
			case 'pending-sent':
				return [{className: 'decline-btn', textContent: 'Cancel Request'}];
			case 'pending-received':
				return [
					{className: 'decline-btn', textContent: 'Decline'},
					{className: 'accept-btn', textContent: 'Accept'},
				];
		}
	}

	async getHTML() {

		const userData = userAPIFriends;

		const friendship = userData.friendship;

		const main = document.querySelector('main');
		main.classList.add('profile', friendship);
		this.setTitle(`${userData.user.username}'s Profile`);
		const userName = profileTitle(userData.user.username);
		const userImg = profileImg(userData.user.img);

		const buttons = this.selectButtons(friendship);
		const actionBar = buttonBar(buttons);
		const userPlacement = arrayToElementsList(userData.placements, 'user-placement', smallPlacementCard);
		const userDescription = profileDescription(userData.user.description);

		const userStats = friendship === "friend"
			? scrollContainer(
				userData.stats,
				profileStats, "row", "stat-list")
			: null;
		userStats?.classList.add('play-stats');

		const userHistory = friendship === "friend"
			? scrollContainer(
				userData.playHistory,
				profilePlayHistory, "col", "history-list")
			: null;
		userHistory?.classList.add('play-history');

		this.updateMain(
			userName,
			userImg,
			actionBar,
			userStats,
			userHistory,
			userPlacement,
			userDescription
		);
	}
}



// TODO: Implement the profile page view

// 3. Set up event handler for friend request buttons
// 4. Set up event handler for accept/decline friend request buttons
// 5. Set up event handler for cancel friend request buttons
// 6. Set up event handler for unfriend buttons
// 7. Set up event handler for invite to game buttons