import AView from "./AView";
import Modal from "../components/modal";
import completeProfileForm from "../components/formComponents/completeProfileForm";

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle("Dashboard");
	}

	async getHTML() {
		const modalContainer = Modal("completeProfile", "bg-secondary", completeProfileForm);

		return modalContainer;
	}
}
