import convertDurationToSeconds from '../../utils/convertDurationToSeconds.js';

const historyDetails = (history) => {
	const details = document.createElement('div');
	details.classList.add('play-history-details');

	const duration = document.createElement('div');
	duration.classList.add('play-history-duration');
	const durationInSeconds = Math.round(convertDurationToSeconds(history.duration));
	duration.textContent = `Duration: ${durationInSeconds} seconds`;

	const ballContacts = document.createElement('div');
	ballContacts.classList.add('play-history-ball-contacts');
	ballContacts.textContent = `Ball Contacts: ${history.ball_contacts}`;

	const ballMaxSpeed = document.createElement('div');
	ballMaxSpeed.classList.add('play-history-ball-max-speed');
	ballMaxSpeed.textContent = `Ball Max Speed: ${history.ball_max_speed}`;

	details.appendChild(duration);
	details.appendChild(ballContacts);
	details.appendChild(ballMaxSpeed);

	return details;
};

const profilePlayHistory = (history) => {
	if (history.length === 0) {
		return (document.createElement('p').textContent = 'No play history to display');
	}
	const playHistoryItem = document.createElement('li');
	const playHistoryMain = document.createElement('div');
	playHistoryMain.classList.add('play-history-main', 'bg-primary');

	const dateObj = new Date(history.date);
	const dateString = dateObj.toDateString();
	const timeString = dateObj.toLocaleTimeString();

	const opponent = document.createElement('div');
	opponent.classList.add('play-history-opponent');
	opponent.textContent = history.opponent;
	playHistoryMain.setAttribute('data-id', `${history.opponentId}`);
	playHistoryMain.appendChild(opponent);

	const playHistoryScore = document.createElement('div');
	playHistoryScore.classList.add('play-history-score');
	playHistoryScore.textContent = `${history.scoreSelf} : ${
		history.scoreOpponent ?? 11 - history.scoreSelf
	}`;
	playHistoryMain.appendChild(playHistoryScore);

	const playHistoryDate = document.createElement('div');
	playHistoryDate.classList.add('play-history-date');
	playHistoryDate.textContent = `${dateString} ${timeString}`;
	playHistoryMain.appendChild(playHistoryDate);

	const rootStyles = getComputedStyle(document.documentElement);
	const acceptColor = rootStyles.getPropertyValue('--accept-color').trim();
	const declineColor = rootStyles.getPropertyValue('--decline-color').trim();
	const outlineColor = history.winner ? acceptColor : declineColor;
	playHistoryItem.style.outline = `2px solid ${outlineColor}`;

	const downArrow = document.createElement('img');
	downArrow.setAttribute('src', './static/assets/img/drop-down-arrow.png');
	playHistoryMain.appendChild(downArrow);

	const playHistoryDetails = historyDetails(history);
	playHistoryItem.appendChild(playHistoryMain);
	playHistoryItem.appendChild(playHistoryDetails);

	return playHistoryItem;
};

export default profilePlayHistory;
