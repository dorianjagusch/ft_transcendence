import ImageButton from "./ImageButton.js";

const appendPlayerButtonBar = (playerCard) => {
	const buttonBar = document.createElement('div');
	buttonBar.classList.add('-button-bar');
	playerCard.appendChild(buttonBar);

	const gearButton = ImageButton('./static/assets/img/gear.png');
	buttonBar.appendChild(gearButton);

	const plusButton = ImageButton('./static/assets/img/plus.png');
	plusButton.classList.add('toggle-user', 'add');
	buttonBar.appendChild(plusButton);

}

const PlayerCard = (playername, userImage, playerId, withButtons) => {
	const playerCard = document.createElement('div');
	playerCard.classList.add('player-card', 'bg-secondary', 'flex-row');
	playerCard.setAttribute('data-user-selected', 'false');
	playerCard.setAttribute('data-player-id', playerId);

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
}

export default PlayerCard
