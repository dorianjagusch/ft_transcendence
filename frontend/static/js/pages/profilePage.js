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
			img: '../../assets/img/default-user.png',
			description:
				'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, aliquid! Reiciendis nobis, dolores optio eaque tempora debitis nulla vel magnam nam soluta quas doloribus sit odit eligendi architecto distinctio voluptas recusandae quos necessitatibus tenetur nisi po',
		};


		const main = document.querySelector('main');
		main.classList.add('profile', userData.friendship);

		this.setTitle(`${userData.username}'s Profile`);
		const userName = profileTitle(userData.username);
		const userImg = profileImg(userData.img);

		const buttons = [
			{className: 'decline-btn', textContent: 'Decline'},
			{className: 'accept-btn', textContent: 'Accept'},
		];

		const actionBar = buttonBar(buttons);

		// Create user placement element
		const userPlacement = document.createElement('div');
		userPlacement.classList.add('user-placement');

		userData.placements.forEach((placement) => {
			const smallPlacementCardElement = smallPlacementCard(
				placement.game + ':',
				placement.place.toString()
			);
			userPlacement.appendChild(smallPlacementCardElement);
		});

		// Create user description element
		const userDescription = profileDescription(userData.description);

		this.updateMain(userName, userImg, actionBar, userPlacement, userDescription);
	}
}
