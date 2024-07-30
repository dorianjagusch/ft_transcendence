const StatLine = (className, label, value, afterText = '') => {
	const line = document.createElement('div');
	line.classList.add(className);
	line.textContent = label;

	const span = document.createElement('span');
	span.textContent = value;
	line.appendChild(span);
	line.textContent += afterText;

	return line;
};

export {StatLine};
