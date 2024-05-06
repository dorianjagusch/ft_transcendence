const GameCard = (game, imgFront, imgBack) => {
	const section = document.createElement('section');
	section.classList.add('flex-col');

	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container', 'border', 'game-card', 'bg-primary');

	const frontImg = document.createElement('img');
	frontImg.src = `./static/assets/img/${imgFront}.png`;
	frontImg.classList.add('front-img');
	modalContainer.appendChild(frontImg);

	const gameImg = document.createElement('img');
	gameImg.src = `./static/assets/img/${imgBack}.png`;
	gameImg.alt = `Image of the game ${game}`;
	gameImg.classList.add('game-img');
	modalContainer.appendChild(gameImg);

	const gameTitle = document.createElement('h2');
	gameTitle.classList.add('modal-title', 'game-title');
	gameTitle.textContent = 'Pong';
	modalContainer.appendChild(gameTitle);

	section.appendChild(modalContainer);

	const createTournamentBtn = document.createElement('button');
	createTournamentBtn.classList.add('primary-btn');
	createTournamentBtn.textContent = 'Create Tournament';
	section.appendChild(createTournamentBtn);

	return section;
};

export {GameCard};