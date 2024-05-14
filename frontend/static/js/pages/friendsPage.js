import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';
import FRIENDSHIPSTATUS from '../constants.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Friends');
	}

	createFriendScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, card);
		scroller.classList.add(tokens, identifier);
		return scroller;
	}

	getHTML() {
		const friendService = new FriendService();

		Promise.all([
			friendService.getAllRequest(FRIENDSHIPSTATUS.FRIEND),
			friendService.getAllRequest(FRIENDSHIPSTATUS.PENDINGRECEIVED)
		])
		.then(([acceptedResponse, pendingResponse]) => {
			let acceptedFriends = acceptedResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));
			let pendingFriends = pendingResponse.map(element => ({
				id: element.id,
				username: element.username,
				img: 'https://unsplash.it/200/200',
				status: element.is_online ? 'online' : 'offline'
			}));

			// Create friend and request scrollers
			const friendScroller = this.createFriendScroller(acceptedFriends, friendCard, 'friends', 'bg-secondary');
			const requestScroller = this.createFriendScroller(pendingFriends, requestCard, 'friend-request', 'bg-secondary');

			// Update main with friend and request scrollers
			this.updateMain(friendScroller, requestScroller);
		})
		.catch(error => {
			console.error('Error:', error);
		})
	}
}
