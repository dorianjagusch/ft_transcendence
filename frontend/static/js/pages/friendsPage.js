import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';

const main = document.querySelector('main');
main.innerHTML = '';

const showFriends = async () => {

	var friendService = new FriendService();
	var friendsResponse = friendService.getAllRequest()
	.catch((error) => {
		console.error(error);
	});

	const friends = [];
	friendsResponse.array.forEach(user =>
		friends.push({
		username: user.username,
		img: "https://unsplash.it/200/200",
		status: "online"
	}));

	const friendScroller = scrollContainer(friends, friendCard);
	friendScroller.classList.add('friends', 'bg-secondary');

	const requestScroller = scrollContainer(friends, requestCard);
	requestScroller.classList.add('friend-request', 'bg-secondary');

	main.appendChild(friendScroller);
	main.appendChild(requestScroller);
}

export default showFriends;
