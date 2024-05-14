const profilePlayHistory = (history) => {

	if (!history){
		return null;
	}
	if (history.length === 0){
		return document.createElement('p').textContent = 'No play history to display';
	}
	const playHistoryItem = document.createElement('li');
	playHistoryItem.classList.add('play-history-item', 'bg-primary');

	const dateObj = new Date(history.date);
	const dateString = dateObj.toDateString();
	const timeString = dateObj.toLocaleTimeString();

	const game = document.createElement('div');
	game.classList.add('play-history-game');
	game.textContent = history.game;
	playHistoryItem.appendChild(game);

	const playHistoryScore = document.createElement('div');
	playHistoryScore.classList.add('play-history-score');
	playHistoryScore.textContent = history.score;
	playHistoryItem.appendChild(playHistoryScore);

	const playHistoryDate = document.createElement('div');
	playHistoryDate.classList.add('play-history-date');
	playHistoryDate.textContent = `${dateString} ${timeString}`;
	playHistoryItem.appendChild(playHistoryDate);

	return playHistoryItem;
};

export default profilePlayHistory;