const friendCard = (friend) => {
	const friendCard = document.createElement('button');
	friendCard.className = 'scroll-element user-card';

	friendCard.setAttribute('data-id', friend.id);;

	const userCardText = document.createElement('div');
	userCardText.className = 'user-card-text';

	const friendImg = document.createElement('img');
	friendImg.src = friend.img;

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = friend.username;

	const userStatus = document.createElement('div');
	userStatus.className = 'status';
	userStatus.setAttribute('data-status', friend.status);

	userCardText.appendChild(userName);
	userCardText.appendChild(userStatus);

	friendCard.appendChild(friendImg);
	friendCard.appendChild(userCardText);

	return friendCard;
};

export { friendCard };
