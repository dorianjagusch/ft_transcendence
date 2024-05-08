const friendCard = ({ id, username, status, img }) => {
	const friendCard = document.createElement('button');
	friendCard.className = 'scroll-element user-card';

	const userId = document.createElement('div');
	userId.className = 'user-id';
	user.setAttribute('data-id', id);
	user.setAttribute('data-visible', 'false');

	const imgElement = document.createElement('img');
	imgElement.src = img;

	const userCardText = document.createElement('div');
	userCardText.className = 'user-card-text';

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = username;

	const userStatus = document.createElement('div');
	userStatus.className = 'status';
	userStatus.setAttribute('data-status', status);

	userCardText.appendChild(userName);
	userCardText.appendChild(userStatus);

	friendCard.appendChild(imgElement);
	friendCard.appendChild(userCardText);
	friendCard.appendChild(userId);
	return friendCard;
};

export { friendCard };
