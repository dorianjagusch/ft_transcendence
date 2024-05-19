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
	}

	acceptHandler(friend) {
		const data = {
			friend_id: friend.id
		}

		console.log(data.friend_id)
		const friendService = new FriendService();
		friendService
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
		console.log("Decline friend ");
		console.log(friend.id)
	}

	createFriendScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, card);
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	createRequestScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) => card(friend, this.acceptHandler, this.declineHandler));
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	async getHTML() {
		const friendService = new FriendService();

		try {
			const acceptedPromise = friendService.getAllRequest(constants.FRIENDSHIPSTATUS.FRIEND);
			const pendingPromise = friendService.getAllRequest(constants.FRIENDSHIPSTATUS.PENDINGRECEIVED);

			const acceptedResponse = await acceptedPromise;
			console.log(acceptedResponse);
			const acceptedFriends = acceptedResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));
			console.log(acceptedFriends);
			const friendScroller = this.createFriendScroller(acceptedFriends, friendCard, 'friends', 'bg-secondary');

			const pendingResponse = await pendingPromise;
			console.log(pendingResponse);
			const pendingFriends = pendingResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));
			console.log(pendingFriends);
			const requestScroller = this.createRequestScroller(pendingFriends, requestCard, 'friend-request', 'bg-secondary');

			this.updateMain(friendScroller, requestScroller);
		} catch (error) {
			console.error('Error:', error);
		}
	}
}
