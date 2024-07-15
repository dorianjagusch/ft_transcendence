function searchResultCard(username, img, id) {
	const searchResultDiv = document.createElement('div');
	searchResultDiv.classList.add('friend-result', 'bg-primary');
	searchResultDiv.setAttribute('data-id', id);

	const avatarImg = document.createElement('img');
	avatarImg.src = img;
	avatarImg.alt = 'Avatar';

	const friendName = document.createElement('p');
	friendName.classList.add('friend-name');
	friendName.textContent = username;

	const friendActions = document.createElement('div');
	friendActions.classList.add('friend-actions');

	const addButton = document.createElement('button');
	addButton.classList.add('add-btn');

	const plusImg = document.createElement('img');
	plusImg.src = './frontend/static/assets/img/plus.png';

	addButton.appendChild(plusImg);
	friendActions.appendChild(addButton);

	searchResultDiv.appendChild(avatarImg);
	searchResultDiv.appendChild(friendName);
	searchResultDiv.appendChild(friendActions);

	return searchResultDiv;
}
