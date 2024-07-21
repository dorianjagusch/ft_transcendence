const OpponentButton = (text) => {
	const opponenButton = document.createElement('button');
	opponenButton.classList.add('primary-btn');
	opponenButton.textContent = text;
	return opponenButton
};

function OpponentSelection() {
	const section = document.createElement('section');
	section.classList.add('opponent-selection', 'bg-secondary', 'flex-col');

	const heading = document.createElement('h3');
	heading.textContent = 'Select your oppponent';
	section.appendChild(heading);

	const aiButton = OpponentButton('AI');
	const localPlayerButton = OpponentButton('Local Player');

	section.appendChild(aiButton);
	section.appendChild(localPlayerButton);

	return section;
}

export {OpponentSelection};
