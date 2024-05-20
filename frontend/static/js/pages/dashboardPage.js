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
import profileSummaryStats from "../components/profileComponents/profileSummaryStats.js";

import userData from "../userAPIData/userAPIDashboard.js";

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle("Dashboard");
	}

	async getHTML() {
		const modalContainer = Modal("completeProfile", "bg-secondary", completeProfileForm);

		this.updateMain(
			modalContainer
		);
	}
}