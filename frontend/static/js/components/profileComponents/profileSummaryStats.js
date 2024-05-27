// stats is user.stats, an array of statsObjs

const SummaryItem = (classNames, textContent) => {
	const article = document.createElement('article');
	article.classList.add(classNames, 'bg-secondary');
	article.textContent = textContent;
	return article;
}

const profileSummaryStats = (stats) => {
	const statsList = document.createElement('section');
	statsList.classList.add('summary');
	let wins = 0;
	let gamesPlayed = 0;
	stats.forEach((stat) => {
		wins += stat.stats.gamesWon;
		gamesPlayed += stat.stats.gamesPlayed;
	});
	const losses = gamesPlayed - wins;

	const winsArticle = SummaryItem('dashboard-item', `${wins} wins`);
	const lossesArticle = SummaryItem('dashboard-item', `${losses} losses`);
	const gamesPlayedArticle = SummaryItem('dashboard-item', `${gamesPlayed} games`);

	statsList.appendChild(winsArticle);
	statsList.appendChild(lossesArticle);
	statsList.appendChild(gamesPlayedArticle);

	return statsList;
}

export default profileSummaryStats;