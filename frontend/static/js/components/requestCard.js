const requestCard = ({img, username}) => {
	const friendCard = document.createElement('div');
	friendCard.className = 'scroll-element request-card';

	const imgElement = document.createElement('img');
	imgElement.src = img;

	const userCardText = document.createElement('p');

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = username;

	userCardText.appendChild(userName);

	friendCard.appendChild(imgElement);
	friendCard.appendChild(userCardText);
	return friendCard;
};

export { requestCard };