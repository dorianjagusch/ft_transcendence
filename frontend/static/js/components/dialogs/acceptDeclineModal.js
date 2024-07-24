import ADialog from "./ADialog.js";
import AcceptForm from "../formComponents/acceptDeclineForm.js";

export default class AcceptDeclineModal extends ADialog {
	constructor(callback, ...callbackArgs) {
		super(new AcceptForm(), null);
		this.appendEventlistenters(callback, callbackArgs);
	}

	appendEventlistenters(callback, callbackArgs) {
		this.dialog.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('accept-btn')) {
				this.dialog.close();
				callback(callbackArgs);
			} else if (e.target.classList.contains('decline-btn')) {
				this.dialog.close();
			}
		}, false);
	}

}