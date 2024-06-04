const Button = (className, textContent, handler) => {
	const buttonElement = document.createElement('button');
	buttonElement.classList.add(className);
	buttonElement.textContent = textContent;
	buttonElement.addEventListener('click', handler);
	return buttonElement;
};

const buttonBar = (buttons) => {
	if (!buttons){
		return;
	}
	const buttonBar = document.createElement('div');
	buttonBar.classList.add('button-bar');

	buttons.forEach(({ className, textContent, handler }) => {
		const button = Button(className, textContent, handler);
		buttonBar.appendChild(button);
	});

	return buttonBar;
};

export default buttonBar;
