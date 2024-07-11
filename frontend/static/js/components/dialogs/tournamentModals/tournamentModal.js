import ADialog from '../ADialog.js';
import { inputNotification } from '../../userNotification.js';
import numberOfPlayersForm from '../../formComponents/numberOfPlayersForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class TournamentModal extends ADialog {
	constructor(parentCallback) {
		super(new numberOfPlayersForm(), new TournamentService());
		this.notify = this.notify.bind(this);
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

	notify(message) {
		const notification = inputNotification(message);
		this.form.form.querySelector('h3').after(notification);
		setTimeout(() => {
			notification.remove();
		}, 3000);
	}

	async createTournament(formData) {
		const tournament = {
			name: formData.tournamentName,
			numberOfPlayers: formData.numberOfPlayers,
		};
		return await this.service.postRequest(tournament);
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			(e) => {
				if (e.target.classList.contains('primary-btn')) {
					e.preventDefault();
					const formData = this.getFormData();
					if (!formData.numberOfPlayers) {
						this.notify('Provide a number of players.');
						return;
					}
					try {
						this.createTournament(formData);
						this.onDataReceived(formData);
					} catch (error) {
						this.notify(error.message);
					}
				}
			},
			false
		);
	}
}
