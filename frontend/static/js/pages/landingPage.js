
import {showLandingPage} from './pages/landingPage.js'
import {showLoginPage} from './pages/loginPage.js'

const main = document.querySelector('main')

async function getLeaderboard() {
	const url = '/leaderboard';
	const response = await fetch(url);
	if (response.status !== 200) {
		throw new Error('Failed to fetch leaderboard');
	}
	const data = await response.json();
	return data;
}


createPlacementCard(entry, index){
	const li = document.createElement('li');
	li.classList.add('scroll-element');
	const placementCard = document.createElement('div');
	placementCard.classList.add('placement-card');

	const userImg = document.createElement('div');
	userImg.classList.add('user-img');
	const profileImg = document.createElement('img');
	profileImg.classList.add('user-img');
	profileImg.src = entry.profileImage;

	userImg.appendChild(profileImg);

	if (index === 0) {
		const victoryWreath = document.createElement('img');
		victoryWreath.classList.add('victory-wreath');
		victoryWreath.src = './static/assets/img/wreath.png';
		userImg.appendChild(victoryWreath);
	}


	const placement = document.createElement('h3');
	placement.classList.add('placement');
	if (index % 10 == 0 && index !== 10) {
		placement.textContent = `${index + 1}st Place`;
	} else if (index % 10 === 1 && index !== 11) {
		placement.textContent = `${index + 1}nd Place`;
	} else if (index % 10 === 2 && index !== 12) {
		placement.textContent = `${index + 1}rd Place`;
	} else {
		placement.textContent = `${index + 1}th Place`;
	}

	if (index < 3){
		const medalImg = document.createElement('img');
		medalImg.classList.add('medal-img');
		medalImg.src = './static/assets/img/gold-medal.png';
	}

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


async function fillLeaderBoard() {
	const leaderboard = await getLeaderboard();
	const placements = document.querySelector('.placements');
	placements.innerHTML = '';
	leaderboard.forEach((entry, index) => {
		const li = createPlacementCard(entry, index);
		placements.appendChild(li);
	});
}


function showLandingPage() {
	const loginButton = document.querySelector('#login');
	loginButton.addEventListener('click', (e) => {
		e.preventDefault();
		showLoginPage();
	});

	const registerButton = document.querySelector('#register');
	registerButton.addEventListener('click', (e) => {
		e.preventDefault();
		showRegisterPage();
	});


	const leaderBoard = document.createElement('section');
	leaderBoard.classList.add('bg-secondary');
	const leaderBoardTitle = '<h2>Leaderboard</h2><ul class="col-scroll placements"></ul></section>';
	leaderBoard.innerHTML = leaderBoardTitle;
	fillLeaderBoard();

	const welcomeSection = document.createElement('section');
	welcomeSection.setAttribute('id', 'welcome');
	const welcomeHtml = '<h2>Welcome</h2><h3>to the great pong tournament</h3>'
	welcomeSection.innerHTML = welcomeHtml;

	main.appendChild(leaderBoard);
	main.appendChild(welcomeSection);
}

export {showLandingPage}