const friendCard = (friend, navigateTo) => {
	const friendCard = document.createElement('button');
	friendCard.className = 'scroll-element user-card';

	const userId = document.createElement('div');
	userId.className = 'user-id';
	user.setAttribute('data-id', friend.id);
	user.setAttribute('data-visible', 'false');

	const userCardText = document.createElement('div');
	userCardText.className = 'user-card-text';

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = friend.username;

	const userStatus = document.createElement('div');
	userStatus.className = 'status';
	userStatus.setAttribute('data-status', friend.status);

	userCardText.appendChild(userName);
	userCardText.appendChild(userStatus);

	friendCard.appendChild(friend.img);
	friendCard.appendChild(userCardText);
	friendCard.appendChild(userId);
	friendCard.addEventListener('click', () => navigateTo(friend));

	return friendCard;
};

export { friendCard };
