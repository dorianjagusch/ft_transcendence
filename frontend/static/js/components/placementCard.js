
const createCardImg = ({profileImage}) => {

	const userImgContainer = document.createElement('div');
	userImgContainer.classList.add('user-img');

	const profileImg = document.createElement('img');
	profileImg.classList.add('user-img');
	profileImg.src = profileImage;
	userImgContainer.appendChild(profileImg);

	if (index === 0) {
		const victoryWreath = document.createElement('img');
		victoryWreath.classList.add('victory-wreath');
		victoryWreath.src = './static/assets/img/wreath.png';
		userImgContainer.appendChild(victoryWreath);
	}

	return userImgContainer;
}

const createPlacement = (index) => {
	document.createElement('h3');
	placement.classList.add('placement');
	if (index % 10 == 0 && index % 100 !== 10) {
		placement.textContent = `${index + 1}st Place`;
	} else if (index % 10 === 1 && index % 100 !== 11) {
		placement.textContent = `${index + 1}nd Place`;
	} else if (index % 10 === 2 && index % 100 !== 12) {
		placement.textContent = `${index + 1}rd Place`;
	} else {
		placement.textContent = `${index + 1}th Place`;
	}
	return placement;
}

const addMedal = (index) => {
	if (index < 3){
		const medalImg = document.createElement('img');
		medalImg.classList.add('medal-img');
		medalImg.src = './static/assets/img/gold-medal.png';
	}
}

const createPlacementCard = (entry, index) => {
	const li = document.createElement('li');
	li.classList.add('scroll-element');
	const placementCard = document.createElement('div');
	placementCard.classList.add('placement-card');


	const userImg = createCardImg(entry);
	const placement = createPlacement(index);
	const medalImg = addMedal(index);

	const user = document.createElement('div');
	user.classList.add('user');
	user.textContent = entry.username;
	const wins = document.createElement('div');
	wins.classList.add('wins');
	wins.textContent = `${entry.wins} wins`;

	placementCard.appendChild(userImg);
	placementCard.appendChild(placement);
	placementCard.appendChild(medalImg);
	placementCard.appendChild(user);
	placementCard.appendChild(wins);

	li.appendChild(placementCard);
}

export default {createPlacementCard}