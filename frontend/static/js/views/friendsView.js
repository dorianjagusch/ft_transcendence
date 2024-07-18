import {friendCard} from '../components/friendCard.js';
import {requestCard} from '../components/requestCard.js';
import {scrollContainer} from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';
import constants from '../constants.js';
import AView from './AView.js';
import getFriendProfilePicture from '../components/friendProfilePicture.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Friends');
		this.friendService = new FriendService();
		this.acceptHandler = this.acceptHandler.bind(this);
		this.declineHandler = this.declineHandler.bind(this);
		this.profileHandler = this.profileHandler.bind(this);
		this.mapResponse = this.mapResponse.bind(this);
	}

	profileHandler(friend) {
		super.navigateTo(`/profile/${friend.id}`);
	}

	acceptHandler(friend) {
		const data = {
			friend_id: friend.id,
		};
		try {
			friendService.postRequest(data).then(() => {
				super.notify('Friendship created successfully.');
				super.navigateTo('/friends');
			});
		} catch (error) {
			super.notify(error);
		}
	}

	declineHandler(friend) {
		try {
			friendService.deleteRequest(friend.id).then(() => {
				super.notify('Friendship declined successfully.');
				super.navigateTo('/friends');
			});
		} catch (error) {
			super.notify(error);
		}
	}

	createFriendScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) => card(friend, this.profileHandler));
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	createRequestScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) =>
			card(friend, this.acceptHandler, this.declineHandler, this.profileHandler)
		);
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	async mapResponse(response) {
		return response.map((element) => {
			const id = element.id;
			try {
				const profileImg = getFriendProfilePicture(id);

				return {
					id: element.id,
					username: element.username,
					img: profileImg,
					status: element.is_online ? 'online' : 'offline',
				};
			} catch (error) {
				console.log('Error getting the profile picture element: ', error);
			}
		});
	};

	async getHTML() {
		let acceptedFriends = [];
		let pendingFriends = [];

		try {
			const acceptedPromise = this.friendService.getAllRequest(
				constants.FRIENDSHIPSTATUS.FRIEND
			);
			const pendingPromise = this.friendService.getAllRequest(
				constants.FRIENDSHIPSTATUS.PENDINGRECEIVED
			);

			const acceptedResponse = await acceptedPromise;
			acceptedFriends = await this.mapResponse(acceptedResponse);

			const pendingResponse = await pendingPromise;
			pendingFriends = await this.mapResponse(pendingResponse);
		} catch (error) {
			console.error('An error occured when retrieving your friends', error);
		}

		const friendTitle = document.createElement('h2');
		friendTitle.textContent = 'Friends';
		const friendScroller = this.createFriendScroller(
			acceptedFriends,
			friendCard,
			'friends',
			'bg-secondary'
		);
		const requestTitle = document.createElement('h2');
		requestTitle.textContent = 'Friend Requests';
		const requestScroller = this.createRequestScroller(
			pendingFriends,
			requestCard,
			'friend-request',
			'bg-secondary'
		);
		this.updateMain(friendTitle, friendScroller, requestTitle, requestScroller);
	}
}
