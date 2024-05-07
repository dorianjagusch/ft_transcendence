import AView from "./AView";

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Friends');
		this.registerHandler = this.registerHandler.bind(this);
	}

	registerHandler = async (e) => {
	};

	appendEventListeners() {
	}

	async getHTML() {
		return;
	}
}

//const showFriends = async () => {
//	const main = document.querySelector('main');
//	main.innerHTML = '';

//	var friendService = new FriendService();
//	var friendsResponse = JSON.parse(friendService.getAllRequest()
//	.catch((error) => {
//		alert("Something went wrong");
//		console.error(error);
//	}));

//	const friends = [];
//	friendsResponse.forEach(user =>
//		friends.push({
//			id: user.id,
//			username: user.username,
//			img: "https://unsplash.it/200/200",
//			status: "online"
//		})
//	);

//	const friendScroller = scrollContainer(friends, friendCard);
//	friendScroller.classList.add('friends', 'bg-secondary');

//	const requestScroller = scrollContainer(friends, requestCard);
//	requestScroller.classList.add('friend-request', 'bg-secondary');

//	main.appendChild(friendScroller);
//	main.appendChild(requestScroller);
//}

//export default showFriends;
