
const createCardImg = ({ img, place }) => {

  const userImgContainer = document.createElement('div');
  userImgContainer.classList.add('user-img');

  const profileImg = document.createElement('img');
  profileImg.classList.add('user-img');
  profileImg.src = img;
  userImgContainer.appendChild(profileImg);

  if ( place === 1) {
    const victoryWreath = document.createElement('img');
    victoryWreath.classList.add('victory-wreath');
    victoryWreath.src = './static/assets/img/wreath.png';
    userImgContainer.appendChild(victoryWreath);
  }

  return userImgContainer;
}

const createPlacement = ({ place }) => {
  const placement = document.createElement('h3');
  placement.classList.add('placement');
  if (place % 10 == 1 && place % 100 !== 11) {
    placement.textContent = `${place}st Place`;
  } else if (place % 10 === 2 && place % 100 !== 12) {
    placement.textContent = `${place}nd Place`;
  } else if (place % 10 === 3 && place % 100 !== 13) {
    placement.textContent = `${place}rd Place`;
  } else {
    placement.textContent = `${place}th Place`;
  }
  return placement;
}

const addMedal = ({ place }) => {
	const medalImg = document.createElement('img');
	switch (place) {
		case 1:
			medalImg.src = './static/assets/img/gold-medal.png';
			break;
		case 2:
			medalImg.src = './static/assets/img/silver-medal.png';
			break;
		case 3:
			medalImg.src = './static/assets/img/bronze-medal.png';
			break;
		default:

	}
	medalImg.classList.add('medal-img');
	return medalImg;
}


function PlacementCard(entry) {
  const placementCard = document.createElement("div");
  placementCard.classList.add("placement-card");

  const userImg = createCardImg(entry);
  const placement = createPlacement(entry);
  const medalImg = addMedal(entry);

  const user = document.createElement("div");
  user.classList.add("user");
  user.textContent = entry.username;
  const wins = document.createElement("div");
  wins.classList.add("wins");
  wins.textContent = `${entry.wins} wins`;

  placementCard.appendChild(userImg);
  placementCard.appendChild(placement);
  placementCard.appendChild(medalImg);
  placementCard.appendChild(user);
  placementCard.appendChild(wins);

  return placementCard;
}

export {PlacementCard}