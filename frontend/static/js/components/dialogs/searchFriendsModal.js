import ADialog from './ADialog.js';
import searchResultCard from '../formComponents/searchResultCard.js';
import UserService from '../../services/userService.js';
import searchFriendsForm from '../formComponents/searchFriendsForm.js';

export default class SearchFriendsModal extends ADialog {
	constructor() {
		super(new searchFriendsForm(), new UserService());
		this.appendEventlistenters();
	}

	//TODO ADD FriendService to determine friend status with the user they are trying to add
			
	appendEventlistenters() {
		const searchFriendsField = this.form.form.querySelector('#friend-name');
		searchFriendsField.addEventListener('input', async () => {
			const searchMatches = await this.service.getRequest(searchFriendsField.value);
			const searchResults = document.querySelector('.search-results');
			searchResults.innerHTML = '';
			searchMatches.forEach((match) => {
				const searchResult = searchResultCard(match.username, match.avatar, match.id);
				searchResults.appendChild(searchResult);
			});
		});
		const searchResults = this.form.form.querySelector('.search-results');
		searchResults.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('add-btn')) {
				const friendId = e.target.closest('.friend-result').dataset.id;
				this.addFriend(friendId);
			}
		});
	}
}
