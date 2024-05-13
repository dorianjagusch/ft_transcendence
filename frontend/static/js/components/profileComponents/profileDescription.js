const profileDescription = (userText) =>{
	const profileDescription = document.createElement('article');
	profileDescription.classList.add('user-description');

	const descriptionTitle = document.createElement('header');
	descriptionTitle.classList.add('description-title');
	descriptionTitle.textContent = 'About: ';

	const descriptionText = document.createElement('p');
	descriptionText.classList.add('description-text');
	descriptionText.textContent = userText;

	profileDescription.appendChild(descriptionTitle);
	profileDescription.appendChild(descriptionText);
	return profileDescription;
}

export default profileDescription;