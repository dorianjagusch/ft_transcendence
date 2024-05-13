import AView from './AView.js';
import buttonBar from '../components/profileComponents/buttonBar.js';
import profileImg from '../components/profileComponents/profileImg.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileDescription from '../components/profileComponents/profileDescription.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';

export default class extends AView {
	constructor(params) {
		super(params);
	}

	async getHTML() {
		const user = {
			id: 1,
			username: 'Username',
			img: './static/assets/img/default-user.png',
			description:
				'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, aliquid! Reiciendis nobis, dolores optio eaque tempora debitis nulla vel magnam nam soluta quas doloribus sit odit eligendi architecto distinctio voluptas recusandae quos necessitatibus tenetur nisi po',
		};

		const statObj1 = {
			game: 'Pong',
			stats: {
				highscore: 100,
				gamesPlayed: 10,
				gamesWon: 5,
			},
		};
		const statObj2 = {
			game: 'Game2',
			stats: {
				highscore: 100,
				gamesPlayed: 10,
				gamesWon: 5,
			},
		};

		const placementObj1 = {
			game: 'Pong',
			place: 1,
		};

		const placementObj2 = {
			game: 'Game2',
			place: 101,
		};

		const historyObj1 = {
			game: 'Pong',
			date: '2021-01-01',
			score: 100,
		};
		const historyObj2 = {
			game: 'Pong',
			date: '2021-01-02',
			score: 100,
		};
		const historyObj3 = {
			game: 'Game2',
			date: '2021-01-03',
			score: 100,
		};
		const historyObj4 = {
			game: 'Pong',
			date: '2021-01-04',
			score: 100,
		};
		const historyObj5 = {
			game: 'Game2',
			date: '2021-01-05',
			score: 100,
		};

		const userData = {
			user,
			friendship: 'pending', // | "friend" | "not-friend" | "pending-sent" | "pending-received"
			placements: [
				//[placementObj, ...] | null
				placementObj1,
				placementObj2,
			],
			stats: [
				// [statObj, ...] | null
				statObj1,
				statObj2,
			],
			playHistory: [
				//[historyObj, ...] | null
				historyObj1,
				historyObj2,
				historyObj3,
				historyObj4,
				historyObj5,
			],
		};

		const main = document.querySelector('main');
		main.classList.add('profile', userData.friendship);
		this.setTitle(`${userData.user.username}'s Profile`);
		const userName = profileTitle(userData.user.username);
		const userImg = profileImg(userData.user.img);

		const buttons = [
			{className: 'decline-btn', textContent: 'Decline'},
			{className: 'accept-btn', textContent: 'Accept'},
		];

		const actionBar = buttonBar(buttons);

		// Create user placement element
		const userPlacement = document.createElement('div');
		userPlacement.classList.add('user-placement');

		userData.placements.forEach((placement) => {
			const smallPlacementCardElement = smallPlacementCard(placement);
			userPlacement.appendChild(smallPlacementCardElement);
		});

		// Create user description element
		const userDescription = profileDescription(userData.user.description);

		this.updateMain(userName, userImg, actionBar, userPlacement, userDescription);
	}
}
