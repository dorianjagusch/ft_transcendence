import { createPlacement } from "../placementCard.js";

const smallPlacementCard = (placementData) => {
	const smallPlacementCard = document.createElement('div');
	smallPlacementCard.classList.add('small-placement-card');

	const gameName = document.createElement('div');
	gameName.classList.add('game');
	gameName.textContent = placementData.game + ':';

	const placementField = document.createElement('div');
	placementField.classList.add('placement');
	placementField.textContent = createPlacement(placementData).textContent;

	smallPlacementCard.appendChild(gameName);
	smallPlacementCard.appendChild(placementField);

	return smallPlacementCard;
};

export default smallPlacementCard;