import ADialog from '../ADialog.js';
import SummaryForm from '../../formComponents/summaryForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class SummaryModal extends ADialog {
	constructor(parentDataHandler, tournamentData) {
		super(new SummaryForm(tournamentData), new TournamentService());
		this.tournamentData = tournamentData;
		this.onDataReceived = parentDataHandler;
	}
}