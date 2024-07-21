const RadioInputField = (label, trait) => {
	const input = document.createElement('input');
	input.setAttribute('type', 'radio');
	input.setAttribute('id', `players-${label}`);
	input.setAttribute('name', trait);
	input.setAttribute('value', label);

	const buttonLabel = document.createElement('label');
	buttonLabel.setAttribute('for', `players-${label}`);
	buttonLabel.textContent = label;

	const radioItem = document.createElement('div');
	radioItem.classList.add('radio-item');
	radioItem.appendChild(input);
	radioItem.appendChild(buttonLabel);
	return radioItem;
};

const RadioSection = (trait, options) => {
	const radioSection = document.createElement('div');
	radioSection.classList.add('menu-item');

	options.forEach((option, index) => {
		const radio = RadioInputField(option, trait);
		if (index == 0){
			radio.querySelector('input').setAttribute('checked', 'checked');
		}
		radioSection.appendChild(radio);
	});

	return radioSection;
}

export default RadioSection;
