const main = document.querySelector('main')

function showLandingPage() {
	const leaderBoard = document.createElement('section');
	leaderBoard.classList.add('bg-secondary');
	const leaderBoardTitle = '<h2>Leaderboard</h2><ul class="col-scroll placements"></ul></section>';
	leaderBoard.innerHTML = leaderBoardTitle;


	const welcomeSection = document.createElement('section');
	welcomeSection.setAttribute('id', 'welcome');
	const welcomeHtml = '<h2>Welcome</h2><h3>to the great pong tournament</h3>'
	welcomeSection.innerHTML = welcomeHtml;
	
	main.appendChild(leaderBoard);
	main.appendChild(welcomeSection);
}

export {showLandingPage}