
const profileImg = (userImg) => {
	const profileImg = document.createElement('div');
	profileImg.classList.add('profile-img');
	userImg.classList.add('user-img');
	userImg.alt = '';
	profileImg.appendChild(userImg);
	return profileImg;
}

export default profileImg;
