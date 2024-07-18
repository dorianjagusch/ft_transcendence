import ADialog from "./ADialog.js";
import AcceptForm from "../formComponents/acceptDeclineForm.js";
import PongService from "../../services/pongService.js";
import { navigateTo } from "../../router.js";

export default class AcceptDeclineModal extends ADialog {
	constructor() {
		super(new AcceptForm(), new PongService());
		this.appendEventlistenters();
	}

	appendEventlistenters() {
		this.dialog.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('accept-btn')) {
				this.dialog.close();
				navigateTo('/pong');
			} else if (e.target.classList.contains('decline-btn')) {
				this.dialog.close();
			}
		}, false);
	}

}