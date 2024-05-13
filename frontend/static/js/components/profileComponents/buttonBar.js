const Button = (className, textContent) => {
	const buttonElement = document.createElement('button');
	buttonElement.classList.add(className);
	buttonElement.textContent = textContent;
	return buttonElement;
};

const buttonBar = (buttons) => {
	const buttonBar = document.createElement('div');
	buttonBar.classList.add('button-bar');

	buttons.forEach(({ className, textContent }) => {
		const button = Button(className, textContent);
		buttonBar.appendChild(button);
	});

	return buttonBar;
};

export default buttonBar;
