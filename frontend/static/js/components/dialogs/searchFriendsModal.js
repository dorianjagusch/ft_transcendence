import ADialog from './ADialog.js';
import searchResultCard from '../formComponents/searchResultCard.js';
import UserService from '../../services/userService.js';
import searchFriendsForm from '../formComponents/searchFriendsForm.js';
import getProfilePicture from '../profilePicture.js';
import FriendService from '../../services/friendService.js';
import {navigateTo} from '../../router.js';
import constants from '../../constants.js';

export default class SearchFriendsModal extends ADialog {
	constructor() {
		super(new searchFriendsForm(), new UserService());
		this.adjustForm = this.adjustForm.bind(this);
		this.adjustForm();
		this.friendService = new FriendService();
		this.addFriend = this.addFriend.bind(this);
		this.deleteFriendRequest = this.deleteFriendRequest.bind(this);
		this.appendEventlistenters();
		this.searchFriendsField;
	}

	adjustForm() {
		const title = document.createElement('h3');
		title.textContent = 'Search for Friends';
		this.form.form.prepend(title);
	}

	selectButtons(relationship) {
		switch (relationship) {
			case constants.FRIENDSHIPSTATUS.FRIEND:
				return null;
			case constants.FRIENDSHIPSTATUS.NOTFRIEND:
				return [
					{
						className: 'accept-btn',
						textContent: 'Add Friend',
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGSENT:
				return [
					{
						className: 'decline-btn',
						textContent: 'Cancel Request',
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGRECEIVED:
				return [
					{
						className: 'decline-btn',
						textContent: 'Decline',
					},
					{className: 'accept-btn', textContent: 'Accept'},
				];
			default:
				return null;
		}
	}

	updateSearchResults(searchMatches) {
		const searchResults = document.querySelector('.search-results');
		searchResults.innerHTML = '';
		if (!searchMatches) {
			searchResults.textContent = 'No results found.';
			return;
		}
		searchMatches.forEach( async (match) => {
			match.img = await getProfilePicture(match.id);
			const searchResult = searchResultCard(match, this.selectButtons);
			searchResults.appendChild(searchResult);
		});
	}

	async refreshSearchResults(searchTerm) {
		searchTerm = searchTerm.trim();
		if (searchTerm.length < 3) {
			return;
		}
		const searchMatches = await this.service.getAllRequest({
			username_contains: searchTerm,
		});
		this.updateSearchResults(searchMatches);
	}

	async addFriend(friendId) {
		try {
			await this.friendService.postRequest({friend_id: friendId});
			await this.refreshSearchResults(this.searchFriendsField.value);
			this.notify('Friend request sent.', 'success');
		} catch (error) {
			this.notify(error.message, 'error');
		}
	}

	async deleteFriendRequest(friendId) {
		try {
			await this.friendService.deleteRequest(friendId);
			await this.refreshSearchResults(this.searchFriendsField.value);
			this.notify('Friendship declined successfully.', 'success');
		} catch (error) {
			this.notify(error.message, 'error');
		}
	}

	searchInputListener() {
		this.searchFriendsField.addEventListener('input', async () => {
			await this.refreshSearchResults(this.searchFriendsField.value);
		});
	}

	searchResultListener() {
		const searchResults = this.form.form.querySelector('.search-results');
		searchResults.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('accept-btn')) {
				const friendId = e.target.closest('.friend-result').dataset.id;
				this.addFriend(friendId);
			} else if (e.target.classList.contains('decline-btn')) {
				const friendId = e.target.closest('.friend-result').dataset.id;
				this.deleteFriendRequest(friendId);
			} else {
				navigateTo(`/profile/${e.target.closest('.friend-result').dataset?.id}`);
			}
		});
	}

	appendEventlistenters() {
		this.searchFriendsField = this.form.form.querySelector('#friend-name');
		this.searchInputListener();
		this.searchResultListener();
	}
}
