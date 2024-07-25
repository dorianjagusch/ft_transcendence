import AView from './AView.js';
import arrayToElementsList from '../components/profileComponents/arrayToElementsList.js';
import buttonBar from '../components/profileComponents/buttonBar.js';
import profileImg from '../components/profileComponents/profileImg.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileDescription from '../components/profileComponents/profileDescription.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';
import {profileStats} from '../components/profileComponents/profileStats.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import constants from '../constants.js';
import {scrollContainer} from '../components/scrollContainer.js';
import UserService from '../services/userService.js';
import FriendService from '../services/friendService.js';
import getProfilePicture from '../components/profilePicture.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.userService = new UserService();
		this.friendService = new FriendService();
		this.acceptHandler = this.acceptHandler.bind(this);
		this.removeHandler = this.removeHandler.bind(this);
		this.declineHandler = this.declineHandler.bind(this);
		this.selectButtons = this.selectButtons.bind(this);
		this.friendId = params.id;
	}

	selectButtons(relationship) {
		switch (relationship) {
			case constants.FRIENDSHIPSTATUS.FRIEND:
				return [
					{
						className: 'decline-btn',
						textContent: 'Remove friend',
						handler: this.removeHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.NOTFRIEND:
				return [
					{
						className: 'accept-btn',
						textContent: 'Add Friend',
						handler: this.acceptHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGSENT:
				return [
					{
						className: 'decline-btn',
						textContent: 'Cancel Request',
						handler: this.declineHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGRECEIVED:
				return [
					{
						className: 'decline-btn',
						textContent: 'Decline',
						handler: this.declineHandler,
					},
					{
						className: 'accept-btn',
						textContent: 'Accept',
						handler: this.acceptHandler
					},
				];
			default:
				return null;
		}
	}

	async acceptHandler() {
		const data = {
			friend_id: this.friendId,
		};

		try {
			await this.friendService.postRequest(data);
			super.notify('Friendship created successfully.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	async removeHandler() {
		try {
			await this.friendService.deleteRequest(this.friendId);
			super.notify('Friendship deleted.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error);
		}
	}

	async declineHandler() {
		try {
			await this.friendService.deleteRequest(this.friendId);
			super.notify('Friendship declined successfully.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	async getHTML() {
		let fakeUser = {
			id: 1,
			username: 'Username',
			img: './static/assets/img/default-user.png',
			description:
				'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, aliquid! Reiciendis nobis, dolores optio eaque tempora debitis nulla vel magnam nam soluta quas doloribus sit odit eligendi architecto distinctio voluptas recusandae quos necessitatibus tenetur nisi po',
			friendship: constants.FRIENDSHIPSTATUS.FRIEND,
		};

		let userResponse;
		try {
			userResponse = await this.userService.getRequest(this.friendId);
			userResponse.img = await getProfilePicture(this.friendId);
		} catch (error) {
			console.notify(error.message, 'error');
			this.navigateTo('/friends');
		}

		const statObj1 = {
			game: 'Pong',
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
			game: 'Pong',
			date: '2021-01-04',
			score: 100,
		};

		const userData = {
			userResponse,
			friendship: 'friend', // | "friend" | "not-friend" | "pending-sent" | "pending-received"
			placements: [
				//[placementObj, ...] | null
				placementObj1,
			],
			stats: [
				// [statObj, ...] | null
				statObj1,
			],
			playHistory: [
				//[historyObj, ...] | null
				historyObj1,
				historyObj2,
				historyObj3,
			],
		};

		const friendship = userResponse.friendship;
		const main = document.querySelector('main');
		main.classList.add('profile', friendship);
		this.setTitle(`${userResponse.username}'s Profile`);
		const userName = profileTitle(userResponse.username);
		const userImg = profileImg(userResponse.img);

		const buttons = this.selectButtons(friendship);
		const actionBar = buttonBar(buttons);
		const userPlacement = arrayToElementsList(
			userData.placements,
			'user-placement',
			smallPlacementCard
		);
		const userDescription = profileDescription(fakeUser.description);

		const userStats =
			friendship === 'friend'
				? scrollContainer(userData.stats, profileStats, 'row', 'stat-list')
				: null;
		userStats?.classList.add('play-stats');

		const userHistory =
			friendship === 'friend'
				? scrollContainer(userData.playHistory, profilePlayHistory, 'col', 'history-list')
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

