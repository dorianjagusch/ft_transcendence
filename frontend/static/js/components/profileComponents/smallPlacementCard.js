import { createPlacement } from "../placementCard.js";

const smallPlacementCard = (placement) => {
	const smallPlacementCard1 = document.createElement('div');
	smallPlacementCard1.classList.add('small-placement-card');
	const game1 = document.createElement('div');
	game1.classList.add('game');
	game1.textContent = 'Pong:';
	const placement1 = document.createElement('div');
	placement1.classList.add('placement');
	placement1.textContent = createPlacement(placement);
	smallPlacementCard1.appendChild(game1);
	smallPlacementCard1.appendChild(placement1);
};

export default smallPlacementCard;