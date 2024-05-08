import {createPlacementCard} from './placementCard.js'
import leaderBoardService from '../services/leaderBoardService.js'

const fillLeaderBoard = async () => {
	const leaderboard = await leaderBoardService.getLeaderboard();
	const placements = document.querySelector('.placements');
	placements.innerHTML = '';
	leaderboard.forEach((entry, index) => {
			const li = createPlacementCard(entry, index);
			placements.appendChild(li);
	});
}

export default {fillLeaderBoard};