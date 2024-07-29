// const history = {
// 	match_id: match.id,
// 	opponent: opponent.username,
// 	opponentId: opponent.id,
// 	winner: self.score > opponent.score,
// 	scoreSelf: self.score,
// 	scoreOpponent: opponent.score,
// };

const profilePlayHistory = (history) => {
	debugger;
	if (history.length === 0) {
		return (document.createElement('p').textContent = 'No play history to display');
	}
	const playHistoryItem = document.createElement('li');
	playHistoryItem.classList.add('play-history-item', 'bg-primary');

	const dateObj = new Date(history.date);
	const dateString = dateObj.toDateString();
	const timeString = dateObj.toLocaleTimeString();

	const opponent = document.createElement('div');
	opponent.classList.add('play-history-opponent');
	opponent.textContent = history.opponent;
	playHistoryItem.setAttribute('data-id', `${history.opponentId}`);
	playHistoryItem.appendChild(opponent);

	const playHistoryScore = document.createElement('div');
	playHistoryScore.classList.add('play-history-score');
	playHistoryScore.textContent = `${history.scoreSelf} : ${
		history.scoreOpponent ?? 11 - history.scoreSelf
	}`;
	playHistoryItem.appendChild(playHistoryScore);

	const playHistoryDate = document.createElement('div');
	playHistoryDate.classList.add('play-history-date');
	playHistoryDate.textContent = `${dateString} ${timeString}`;
	playHistoryItem.appendChild(playHistoryDate);

	const rootStyles = getComputedStyle(document.documentElement);
	const acceptColor = rootStyles.getPropertyValue('--accept-color').trim();
	const declineColor = rootStyles.getPropertyValue('--decline-color').trim();
	const outlineColor = history.winner ? acceptColor : declineColor;
	playHistoryItem.style.outline = `2px solid ${outlineColor}`;

	return playHistoryItem;
};

export default profilePlayHistory;
