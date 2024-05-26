const requestOptions = (user, acceptRequest, declineRequest) => {
	const options = document.createElement('div');
	options.classList.add('request-options');

	const acceptButton = document.createElement('button');
	acceptButton.classList.add('check-btn');
	acceptButton.addEventListener('click', () => acceptRequest(user));

	const declineButton = document.createElement('button');
	declineButton.classList.add('x-btn');
	declineButton.addEventListener('click', () => declineRequest(user));

	options.appendChild(acceptButton);
	options.appendChild(declineButton);
	return options;
};

const requestCard = (request, acceptRequest, declineRequest) => {
	const card = document.createElement('div');
	card.className = 'scroll-element request-card';

	const imgElement = document.createElement('img');
	imgElement.src = request.img;

	const userCardText = document.createElement('p');

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = request.username;

	userCardText.appendChild(userName);

	card.append(imgElement, userCardText, requestOptions(request, acceptRequest, declineRequest));
	return card;
};

export { requestCard };

