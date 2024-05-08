const SpanLine = (text, id) => {
	const spanLine = document.createElement('p');
	spanLine.textContent = text + ': ';
	const span = document.createElement('span');
	span.id = id;
	spanLine.appendChild(span);
	return spanLine;
};

const PongContainer = () => {
	const pongContainer = document.createElement('div');
	pongContainer.id = 'pong-container';

	const pongOptions = [
		{ text: 'Room name', id: 'room-name' },
		{ text: 'Player 1', id: 'player-one-position' },
		{ text: 'Player 2', id: 'player-two-position' },
		{ text: 'Ball', id: 'ball-position' },
		{ text: 'Score player 1', id: 'score1' },
		{ text: 'Score player 2', id: 'score2' },
		{ text: 'Key pressed', id: 'key-pressed' },
		{ text: 'Received', id: 'received' },
	];

	pongOptions.forEach((option) => {
		const spanLine = SpanLine(option.text, option.id);
		pongContainer.appendChild(spanLine);
	});

	return pongContainer;
};

const Pong = () => {
	const pong = document.createElement('div');
	pong.id = 'pong';

	const pongContainer = PongContainer();
	pong.appendChild(pongContainer);

	return pong;
};

const showPong = () => {
	const main = document.querySelector('main');
	const pong = Pong();
	main.appendChild(pong);
	document.getElementById('room-name').textContent = "room"; //change the roomname here. if you need it as a separate request already, lmk
};


export default showPong;