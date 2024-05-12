
const profileImg = (img) => {
	const profileImg = document.createElement('div');
	profileImg.classList.add('profile-img');
	const userImg = document.createElement('img');
	userImg.classList.add('user-img');
	userImg.src = 'img';
	userImg.alt = '';
	profileImg.appendChild(userImg);
}

export default profileImg;