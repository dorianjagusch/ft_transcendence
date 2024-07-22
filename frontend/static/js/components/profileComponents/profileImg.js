
const profileImg = (userImgSrc) => {
	const profileImg = document.createElement('div');
	profileImg.classList.add('profile-img');
	const userImg = document.createElement('img');
	userImg.classList.add('user-img');
	userImg.src = userImgSrc;
	profileImg.appendChild(userImg);
	return profileImg;
}

export default profileImg;
