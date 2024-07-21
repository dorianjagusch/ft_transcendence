import ADialog from '../ADialog.js';
import SummaryForm from '../../formComponents/summaryForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class SummaryModal extends ADialog {
	constructor(parentDataHandler, tournamentData) {
		super(new SummaryForm(tournamentData), new TournamentService());
		this.tournamentData = tournamentData;
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			async (e) => {
				if (e.target.classList.contains('accept-btn')) {
					e.preventDefault();
					try {
						const TournamentData = await this.service.getRequest(this.tournamentData.id);
						this.onDataReceived(TournamentData);
					} catch (error) {
						this.notify(error.message);
					}
				}
			},
			false
		);
	}
}
