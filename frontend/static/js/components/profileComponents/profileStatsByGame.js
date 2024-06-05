import {StatLine} from './profileStats.js';

const profileStatsByGame = ({game, stats}, number) => {
	const title = document.createElement('h4');
	title.textContent = game;

	const wins = StatLine('stat-entry', '', stats.gamesWon, ' wins');
	const gamesPlayed = StatLine('stat-entry', 'Played ', stats.gamesPlayed, ' games');
	const losses = StatLine('stat-entry', '', stats.gamesPlayed - stats.gamesWon, ' losses');

	const statsElement = document.createElement('section');
	statsElement.classList.add('stats', `stats-${number}`, 'flex-col');

	statsElement.appendChild(title);
	statsElement.appendChild(wins);
	statsElement.appendChild(losses);
	statsElement.appendChild(gamesPlayed);

	return statsElement;
};

export default profileStatsByGame;
