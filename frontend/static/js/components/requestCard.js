const requestOptions = (acceptRequest, declineRequest) => {
	const options = document.createElement('div');
	options.classList.add('request-options');

	const acceptButton = document.createElement('button');
	acceptButton.classList.add('check-btn');
	acceptButton.addEventListener('click', acceptRequest);

	const declineButton = document.createElement('button');
	declineButton.classList.add('x-btn');
	declineButton.addEventListener('click', declineRequest);

	options.appendChild(acceptButton);
	options.appendChild(declineButton);
	return options;
};

const requestCard = ({ img, username }, acceptRequest, declineRequest) => {
	const card = document.createElement('div');
	card.className = 'scroll-element request-card';

	const imgElement = document.createElement('img');
	imgElement.src = img;

	const userCardText = document.createElement('p');

	const userName = document.createElement('div');
	userName.className = 'user-name';
	userName.innerText = username;

	userCardText.appendChild(userName);

	card.append(imgElement, userCardText, requestOptions(acceptRequest, declineRequest));
	return card;
};

export { requestCard };

