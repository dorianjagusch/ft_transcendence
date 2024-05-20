// stats is user.stats, an array of statsObjs

const profileSummaryStats = (stats) => {
	const statsList = document.createElement('section');
	statsList.className = 'summary';
	let statsArray = Object.entries(stats);
	let wins = 0;
	let gamesPlayed = 0;
	statsArray.forEach((stat) => {
		wins += stats.gamesWon;
		gamesPlayed += stats.gamesPlayed;
	});
	const losses = gamesPlayed - wins;

	const winsArticle = document.createElement('article');
	winsArticle.className = 'dashboard-item wins';
	winsArticle.textContent = `${wins} wins`;

	const lossesArticle = document.createElement('article');
	lossesArticle.className = 'dashboard-item losses';
	lossesArticle.textContent = `${losses} losses`;

	const gamesPlayedArticle = document.createElement('article');
	gamesPlayedArticle.className = 'dashboard-item games-played';
	gamesPlayedArticle.textContent = `${gamesPlayed} games`;

	statsList.appendChild(winsArticle);
	statsList.appendChild(lossesArticle);
	statsList.appendChild(gamesPlayedArticle);

	return statsList;
}

export default profileSummaryStats;