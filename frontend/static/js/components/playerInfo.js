import {StatLine} from './profileComponents/profileStats.js';

const PlayerInfo = ({username, img, stats}) => {
	const section = document.createElement('section');
	section.classList.add('player-info', 'bg-secondary', 'flex-col');

	const usernameElement = document.createElement('h3');
	usernameElement.id = 'username';
	usernameElement.textContent = username;
	section.appendChild(usernameElement);

	const imgElement = document.createElement('img');
	imgElement.src = img;
	imgElement.alt = 'Profile Picture';
	imgElement.classList.add('profile-picture');
	section.appendChild(imgElement);

	const winsDiv = StatLine('wins', 'Wins: ', stats.wins);
	section.appendChild(winsDiv);

	const lossesDiv = StatLine('losses', 'Losses: ', stats.losses);
	section.appendChild(lossesDiv);

	const ratioDiv = StatLine(
		'win-loss-ratio',
		'W/L ratio: ',
		stats.wins + stats.losses ? (stats.wins / (stats.wins + stats.losses)).toFixed(2) : 'NA'
	);
	section.appendChild(ratioDiv);

	return section;
};

export {PlayerInfo};
