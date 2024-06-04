
const StatLine = (className, label, value, afterText = '') => {
	const line = document.createElement('div');
	line.classList.add(className);
	line.textContent = label;

	const span = document.createElement('span');
	span.textContent = value;
	line.appendChild(span);
	line.textContent += afterText;

	return line;
};

const profileStats = ({game, stats}) => {

	const gameName = document.createElement('h4');
	gameName.classList.add('game-name');
	gameName.textContent = game;

	const stat = document.createElement('li');
	stat.classList.add('stat-item', 'bg-primary');

	const highscore = StatLine('highscore', 'Highscore: ', stats.highscore);
	const wins = StatLine('wins', 'Won ', stats.gamesWon, ' times');
	const gamesPlayed = StatLine('games-played', 'Played ', stats.gamesPlayed, ' times');

	stat.appendChild(gameName);
	stat.appendChild(highscore);
	stat.appendChild(wins);
	stat.appendChild(gamesPlayed);
	return stat;
};

export {
	profileStats,
	StatLine
};