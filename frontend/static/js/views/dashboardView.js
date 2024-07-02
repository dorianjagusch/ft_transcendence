import AView from "./AView.js";
import Modal from "../components/modal.js";
import completeProfileForm from "../components/formComponents/completeProfileForm.js";
import profileTitle from "../components/profileComponents/profileTitle.js";
import profileImg from "../components/profileComponents/profileImg.js";
import arrayToElementsList from '../components/profileComponents/arrayToElementsList.js';
import profileDescription from "../components/profileComponents/profileDescription.js";
import smallPlacementCard from "../components/profileComponents/smallPlacementCard.js";
import { scrollContainer } from "../components/scrollContainer.js";
import profilePlayHistory from "../components/profileComponents/profilePlayHistory.js";
import profileStatsByGame from "../components/profileComponents/profileStatsByGame.js"
import profileSummaryStats from "../components/profileComponents/profileSummaryStats.js";
import userData from "../userAPIData/userAPIDashboard.js";
import { profileStats } from "../components/profileComponents/profileStats.js";

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle("Dashboard");
	}

	async getHTML() {

		const title = profileTitle("Your Stats");
		const userImg = profileImg(userData.user.img);

		const userPlacement = arrayToElementsList(userData.placements, "placements", smallPlacementCard);
		userPlacement.classList.add('flex-col')
		const userDescription = profileDescription(userData.user.description);

		const userHistory = scrollContainer(userData.playHistory, profilePlayHistory, "column");
		userHistory.classList.add('play-history');

		const userStats = userData.stats.map((game, index) => {
			const statsEntry = profileStatsByGame(game, index + 1);
			return statsEntry;
		});

		const main = document.querySelector("main");
		main.classList.add("profile", "dashboard");
		this.updateMain(
			title,
			userImg,
			userPlacement,
			userDescription,
			...userStats,
			// gameGraph1,
			userHistory
		);
	}
}
