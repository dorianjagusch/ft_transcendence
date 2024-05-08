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

	async getHTML() {
		// TODO: Use the actual response
		// var friendService = new FriendService();
		//var friendResponse = friendService.getAllRequest()
		//.catch((error) => {
		//	console.error(error);
		//});

		const fakeFriendsResponse = [
			{ id: 1, username: "meri" },
			{ id: 2, username: "azar" },
			{ id: 3, username: "jose" }
		  ];

		const friends = [];
		fakeFriendsResponse.forEach(element => {
			friends.push({
				id: element.id,
				username: element.username,
				img: "https://unsplash.it/200/200",
				status: "online"
			});
		});
		// const friends = Call friendsAPI	to	get	friends in a json array

		const friendScroller = scrollContainer(friends, friendCard);
		friendScroller.classList.add('friends', 'bg-secondary');

		const requestScroller = scrollContainer(friends, requestCard);
		requestScroller.classList.add('friend-request', 'bg-secondary');

		this.updateMain(friendScroller, requestScroller);
	}
}
