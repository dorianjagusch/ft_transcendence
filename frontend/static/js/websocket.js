

const ChatSocket = () => {
	// const roomName = document.getElementById('room-name').textContent // ADD ROOM NAME
	// JSON.parse(
	// 	document.getElementById('room-name').textContent;
	// );

	const chatSocket = new WebSocket(
		'ws://' + window.location.host + ':8080/ws/pong/' // + roomName + '/' //ADD ROOM NAME
	);

	chatSocket.addEventListener('message', (e) => {
		const data = JSON.parse(e.data);
		document.querySelector('#received').value += data.message + '\n';
	});

	chatSocket.addEventListener('close', (e) => {
		console.error('Chat socket closed unexpectedly');
	});

	chatSocket.addEventListener('error', (e) => {
		console.error('Chat socket error:', e);
	});

	document
		.querySelector('#key-pressed')
		.addEventListener('click', (e) => {
			const keyPressed = document.querySelector('#key-pressed');
			const key = keyPressed.value;
			chatSocket.send(
				JSON.stringify({
					message: key,
				})
			);
			keyPressed.value = '';
		});

	return chatSocket;
};

export default ChatSocket;
