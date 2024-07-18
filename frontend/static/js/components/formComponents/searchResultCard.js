import buttonBar from '../profileComponents/buttonBar.js';

const searchResultCard = ({username, img, id, relationship}, buttonSelector) => {
	const searchResult = document.createElement('div');
	searchResult.classList.add('friend-result', 'bg-primary');
	searchResult.setAttribute('data-id', id);

	const avatarImg = document.createElement('img');
	avatarImg.src = img;
	avatarImg.alt = 'Avatar';

	const friendName = document.createElement('p');
	friendName.classList.add('friend-name');
	friendName.textContent = username;

	const friendActions = buttonBar(buttonSelector(relationship));

	searchResult.appendChild(avatarImg);
	searchResult.appendChild(friendName);
	searchResult.appendChild(friendActions);

	return searchResult;
};

export default searchResultCard;
