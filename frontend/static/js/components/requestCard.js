const requestOptions = () => {
	const options = document.createElement('div');
	options.classList.add('request-options');

	const acceptButton = document.createElement('button');
	acceptButton.classList.add('check-btn');

	const declineButton = document.createElement('button');
	declineButton.classList.add('x-btn');

	options.appendChild(acceptButton);
	options.appendChild(declineButton);
	return options;
};

const requestCard = (request) => {
	const card = document.createElement('div');
	card.className = 'scroll-element request-card';
	card.setAttribute('data-id', request.id);
	
	const img = document.createElement('img');
	img.src = request.img;
	const userCardText = document.createElement('p');

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = request.username;

	userCardText.appendChild(userName);

	card.append(img, userCardText, requestOptions());

	return card;
};

export { requestCard };

