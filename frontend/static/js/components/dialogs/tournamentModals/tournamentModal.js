import ADialog from '../ADialog.js';
import numberOfPlayersForm from '../../formComponents/numberOfPlayersForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class TournamentModal extends ADialog {
	constructor(parentCallback) {
		super(new numberOfPlayersForm(), new TournamentService());
		this.getFormData = this.getFormData.bind(this);
		this.onDataReceived = parentCallback;
		this.appendEventlistenters();
		this.radioString = 'input[name="number-of-players"]:checked';
	}

	getFormData() {
		const form = this.form.getForm();
		const tournamentName = form.querySelector('#tournament-name').value;
		const numberOfPlayers = form.querySelector(this.radioString).value;
		return {tournamentName, numberOfPlayers};
	}

	async createTournament(formData) {
		const tournament = {
			custom_name: formData.tournamentName,
			id: 1,
			player_amount: formData.numberOfPlayers,
			player_ids: [1, 5, 3, 2, 6, 4, 7]
		};
		// return await this.service.postRequest(tournament);
		return tournament;
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			async (e) => {
				if (e.target.classList.contains('primary-btn')) {
					e.preventDefault();
					const formData = this.getFormData();
					try {
						const TournamentData = await this.createTournament(formData);
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