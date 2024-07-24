import ADialog from '../ADialog.js';
import SummaryForm from '../../formComponents/summaryForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class SummaryModal extends ADialog {
	constructor(parentDataHandler, tournamentData) {
		super(new SummaryForm(tournamentData), new TournamentService());
		this.tournamentData = tournamentData;
		this.onDataReceived = parentDataHandler;
		this.appendEventlistenters = this.appendEventlistenters.bind(this);
		this.appendEventlistenters();
	}

	appendEventlistenters() {
		this.dialog.addEventListener('click', async (e) => {
			if (e.target.classList.contains('accept-btn')) {
				e.preventDefault();
				try {
					const matchData = await this.service.patchRequest(this.tournamentData);
					this.onDataReceived(matchData);
				} catch (error) {
					this.notify(error.message);
				}
			} else if (e.target.classList.contains('decline-btn')) {
				e.preventDefault();
				this.summaryModal.dialog.close();
				this.selectPlayersModal.dialog.showModal();
			}
		});
	}
}
