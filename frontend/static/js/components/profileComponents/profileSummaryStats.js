// stats is user.stats, an array of statsObjs

const SummaryItem = (classNames, textContent) => {
	const article = document.createElement('article');
	article.classList.add(classNames, 'bg-secondary');
	article.textContent = textContent;
	return article;
};

const profileSummaryStats = ({
	wins,
	losses,
	total_games_played,
	win_loss_ratio,
	winning_streak,
	position_in_leaderBoard,}) => {
	const statsList = document.createElement('section');
	statsList.classList.add('summary');
	const RankArticle = SummaryItem('dashboard-item', `Rank ${position_in_leaderBoard || 'N/A'}`);
	const winsArticle = SummaryItem('dashboard-item', `${wins} wins`);
	const lossesArticle = SummaryItem('dashboard-item', `${losses} losses`);
	const wlRatio = SummaryItem('dashboard-item', `W/G: ${total_games_played === 0 ? 'N/A' : win_loss_ratio}`);
	const gamesPlayedArticle = SummaryItem('dashboard-item', `${total_games_played || 0} games played`);
	const streak = SummaryItem('dashboard-item', `Streak of ${winning_streak}`);

	statsList.append(RankArticle, winsArticle, lossesArticle, wlRatio, gamesPlayedArticle, streak);

	return statsList;
};

export default profileSummaryStats;
