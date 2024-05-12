
const profileTitle = (title) => {
	const profileName = document.createElement('div');
	profileName.classList.add('profile-title');
	profileName.textContent = title;
	return profileName;
};

export default profileTitle;