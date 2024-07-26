import {scrollContainer} from '../components/scrollContainer.js';
import {PlacementCard} from '../components/placementCard.js';
import AView from './AView.js';
import LeaderBoardService from '../services/leaderBoardService.js';
import UserService from '../services/userService.js';
import getProfilePicture from '../components/profilePicture.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Leaderboard');
		this.leaderBoardService = new LeaderBoardService();
		this.userService = new UserService();
		this.appendEventListeners = this.appendEventListeners.bind(this);
	}

	async getPlayers() {
		try {
			const playerData = await this.leaderBoardService.getLeaderBoard();
			const players = [];

			for (const [index, player] of playerData.entries()) {
				if (player.wins == 0) {
					break;
				}
				const img = await getProfilePicture(player.user);
				const userData = await this.userService.getRequest(player.user);
				const username = userData.username;
				players.push({
					username: username,
					userId: player.user,
					wins: player.wins,
					img: img,
					place: index + 1,
				});
			}

			return players;
		} catch (error) {
			this.notify(error, 'error');
			return null;
		}
	}

	appendEventListeners() {
		document.querySelector('.col-scroll').addEventListener('click', (e) => {
			e.preventDefault();
			e.stopPropagation();
			console.log('clicked button');
			const card = e.target.closest('.placement-card');
			if (!card) {
				return;
			}
			const userId = card.getAttribute('data-user-id');
			this.navigateTo(`/profile/${userId}`);
		});
	}

	async getHTML() {
		const players = await this.getPlayers();
		if (!players) {
			return 'No data yet';
		}
		const leaderBoardOne = scrollContainer(players, PlacementCard, 'col');
		leaderBoardOne.classList.add('leaderboard', 'bg-secondary');
		const header = document.createElement('h2');
		header.textContent = 'Leaderboard';
		leaderBoardOne.insertBefore(header, leaderBoardOne.firstChild);
		const innerScroller = leaderBoardOne.querySelector('.col-scroll');
		innerScroller.style.gridAutoRows = '5em';
		this.updateMain(leaderBoardOne);
		this.appendEventListeners();
	}
}
