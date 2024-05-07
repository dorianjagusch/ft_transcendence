import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import FriendService from '../services/friendService.js';
import UserService from '../services/userService.js';

const showFriends = async () => {
	const main = document.querySelector('main');
	main.innerHTML = '';

	var friendService = new FriendService();
	var friendsResponse = JSON.parse(friendService.getAllRequest()
	.catch((error) => {
		alert("Something went wrong");
		console.error(error);
	}));

	const users = [];
	var userService = new UserService();
	friendsResponse.array.forEach(friend =>
		users.push(userService.getRequest(friend.friend_id)
			.catch((error) => {
				alert("Something went wrong");
				console.error(error);
			})
		)
	);

	const friends = [];
	users.forEach(user =>
		friends.push({
			username: user.username,
			img: "https://unsplash.it/200/200",
			status: "online"
		})
	);

	const friendScroller = scrollContainer(friends, friendCard);
	friendScroller.classList.add('friends', 'bg-secondary');

	const requestScroller = scrollContainer(friends, requestCard);
	requestScroller.classList.add('friend-request', 'bg-secondary');

	main.appendChild(friendScroller);
	main.appendChild(requestScroller);
}

export default showFriends;
