import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';
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

	async getHTML() {
		const friendService = new FriendService();
		let friends = [];
		friendService.getAllRequest()
		.then(friendsResponse => {
			friendsResponse.forEach(element => {
				let status = 'offline';
				if (element.is_online) {
					status = 'online';
				}

				friends.push({
					id: element.id,
					username: element.username,
					img: 'https://unsplash.it/200/200',
					status: status
				});
			});

			console.log(friends);

			const friendScroller = this.createFriendScroller(friends, friendCard, 'friends', 'bg-secondary');
			// TODO: Add functionality for pending / possible friendships
			const requestScroller = this.createFriendScroller(friends, requestCard, 'friend-request', 'bg-secondary');
			this.updateMain(friendScroller, requestScroller);
		})
	}
}
