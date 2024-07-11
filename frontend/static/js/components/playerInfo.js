import { StatLine } from "./profileComponents/profileStats.js";

const PlayerInfo = ({username, img, wins, losses}) => {
	const section = document.createElement('section');
	section.classList.add('player-info', 'bg-secondary', 'flex-col');

	const usernameElement = document.createElement('h3');
	usernameElement.id = 'username';
	usernameElement.textContent = username;
	section.appendChild(usernameElement);

	const imgElement = document.createElement('img');
	imgElement.src = img;
	section.appendChild(imgElement);

	const winsDiv = StatLine('wins', 'Wins: ', wins);
	section.appendChild(winsDiv);

	const lossesDiv = StatLine('losses', 'Losses: ', losses);
	section.appendChild(lossesDiv);

	const ratioDiv = StatLine('win-loss-ratio', 'W/L ratio: ', (wins+losses)? (wins / wins+losses).toFixed(2): "NA");
	section.appendChild(ratioDiv);

	return section;
}

export {PlayerInfo}