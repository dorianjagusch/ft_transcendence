
const profileImg = (imgPath) => {
	const profileImg = document.createElement('div');
	profileImg.classList.add('profile-img');
	const userImg = document.createElement('img');
	userImg.classList.add('user-img');
	userImg.src = imgPath;
	userImg.alt = '';
	profileImg.appendChild(userImg);
	return profileImg;
}

export default profileImg;