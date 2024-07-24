import ImageButton from './ImageButton.js';

const resetCard = (clickedCard) => {
	clickedCard.removeAttribute('data-fetching');
	clickedCard.removeAttribute('data-player-id');
	clickedCard.querySelector('.player-name').textContent = 'Add Participant';
	clickedCard.querySelector('.player-img').src = '../static/assets/img/default-user.png';
	clickedCard.querySelector('.toggle-user > img').src = '../static/assets/img/plus.png';
	clickedCard.classList.add('bg-inactive');
	clickedCard.setAttribute('data-user-selected', 'false');

	const button = clickedCard.querySelector('.remove');
	button.classList.toggle('add');
	button.classList.toggle('remove');

	clickedCard.querySelector('.gear').style.visibility = 'hidden';
};

const updateCard = (clickedCard, userData) => {
	clickedCard.removeAttribute('data-fetching');
	clickedCard.setAttribute('data-player-id', userData.id);
	clickedCard.querySelector('.player-name').textContent = userData.display_name;
	clickedCard.querySelector('.player-img').src = userData.img;
	clickedCard.querySelector('.toggle-user > img').src = '../static/assets/img/minus.png';
	clickedCard.classList.remove('bg-inactive');
	clickedCard.setAttribute('data-user-selected', 'true');

	const button = clickedCard.querySelector('.add');
	button.classList.toggle('add');
	button.classList.toggle('remove');

	clickedCard.querySelector('.gear').style.visibility = '';
};

const appendPlayerButtonBar = (playerCard) => {
	const buttonBar = document.createElement('div');
	buttonBar.classList.add('-button-bar');
	playerCard.appendChild(buttonBar);

	const gearButton = ImageButton('./static/assets/img/gear.png');
	gearButton.style.visibility = 'hidden';
	gearButton.classList.add('gear');
	buttonBar.appendChild(gearButton);

	const plusButton = ImageButton('./static/assets/img/plus.png');
	plusButton.classList.add('toggle-user', 'add');
	buttonBar.appendChild(plusButton);
};

const PlayerCard = (playername, userImage, modalId, withButtons) => {
	const playerCard = document.createElement('div');
	playerCard.classList.add('player-card', 'bg-secondary', 'flex-row');
	playerCard.setAttribute('data-user-selected', 'false');
	playerCard.setAttribute('data-modal-id', modalId);

	const image = document.createElement('img');
	image.src = userImage;
	image.classList.add('player-img');
	playerCard.appendChild(image);

	const playerName = document.createElement('div');
	playerName.classList.add('player-name');
	playerName.textContent = playername;
	playerCard.appendChild(playerName);

	if (withButtons) {
		appendPlayerButtonBar(playerCard);
	}

	return playerCard;
};

export {PlayerCard, updateCard, resetCard};
