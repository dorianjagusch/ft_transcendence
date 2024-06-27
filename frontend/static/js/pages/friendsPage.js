import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';
import constants from '../constants.js';
import AView from './AView.js';

export default class extends AView {

	constructor(params) {
		super(params);
		this.setTitle('Friends');
		this.friendService = new FriendService();
		this.acceptHandler = this.acceptHandler.bind(this);
		this.declineHandler = this.declineHandler.bind(this);
		this.profileHandler = this.profileHandler.bind(this);
	}

	profileHandler(friend)	{
		super.navigateTo(`/profile/${friend.id}`);
	}

	acceptHandler(friend) {
		const data = {
			friend_id: friend.id
		}
		this.friendService
			.postRequest(data)
			.then(() => {
				super.notify('Friendship created successfully.');
				super.navigateTo('/friends');
			})
			.catch((error) => {
				super.notify(error);
			});
	}

	declineHandler(friend) {
		this.friendService
			.deleteRequest(friend.id)
			.then(() => {
				super.notify('Friendship declined successfully.');
				super.navigateTo('/friends');
			})
			.catch((error) => {
				super.notify(error);
			});
	}

	createFriendScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) => card(friend, this.profileHandler));
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	createRequestScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) => card(friend, this.acceptHandler, this.declineHandler, this.profileHandler));
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	async getHTML() {
		let acceptedFriends = [];
		let pendingFriends = [];

		try {
			const acceptedPromise = this.friendService.getAllRequest(constants.FRIENDSHIPSTATUS.FRIEND);
			const pendingPromise = this.friendService.getAllRequest(constants.FRIENDSHIPSTATUS.PENDINGRECEIVED);

			const acceptedResponse = await acceptedPromise;
			acceptedFriends = acceptedResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));

			const pendingResponse = await pendingPromise;
			pendingFriends = pendingResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));
		} catch (error) {
			console.error('Error:', error);
		}

		const friendTitle = document.createElement('h2');
		friendTitle.textContent = 'Friends';
		const friendScroller = this.createFriendScroller(acceptedFriends, friendCard, 'friends', 'bg-secondary');
		const requestTitle = document.createElement('h2');
		requestTitle.textContent = 'Friend Requests';
		const requestScroller = this.createRequestScroller(pendingFriends, requestCard, 'friend-request', 'bg-secondary');
		this.updateMain(friendTitle, friendScroller, requestTitle, requestScroller);
	}
}
