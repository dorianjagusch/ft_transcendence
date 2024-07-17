import ADialog from './ADialog.js';
import searchResultCard from '../formComponents/searchResultCard.js';
import UserService from '../../services/userService.js';
import searchFriendsForm from '../formComponents/searchFriendsForm.js';
import FriendService from '../../services/friendService.js';
import {navigateTo} from '../../router.js';
import constants from '../../constants.js'; //TODO: remove once backend send relationship with search results

export default class SearchFriendsModal extends ADialog {
	constructor() {
		super(new searchFriendsForm(), new UserService());
		this.adjustForm = this.adjustForm.bind(this);
		this.adjustForm();
		this.friendService = new FriendService();
		this.addFriend = this.addFriend.bind(this);
		this.deleteFriendRequest = this.deleteFriendRequest.bind(this);
		this.appendEventlistenters();
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

	async addFriend(friendId) {
		try {
			await this.friendService.postRequest({friend_id: friendId});
			this.notify('Friend request sent.');
		} catch (error) {
			this.notify(error);
		}
	}

	async deleteFriendRequest(friendId) {
		try {
			await this.friendService.deleteRequest(friendId);
			this.notify('Friendship declined successfully.');
		} catch (error) {
			this.notify(error);
		}
	}

	searchInputLister() {
		const searchFriendsField = this.form.form.querySelector('#friend-name');
		searchFriendsField.addEventListener('input', async () => {
			const searchMatches = await this.service.getAllRequest();
			const searchResults = document.querySelector('.search-results');
			searchResults.innerHTML = '';
			searchMatches.forEach((match) => {
				match.relationship = constants.FRIENDSHIPSTATUS.NOTFRIEND;
				const searchResult = searchResultCard(match, this.selectButtons);
				searchResults.appendChild(searchResult);
			});
		});
	}

	searchResultListener() {
		const searchResults = this.form.form.querySelector('.search-results');
		searchResults.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('accept-btn')) {
				e.stopPropagation();
				const friendId = e.target.closest('.friend-result').dataset.id;
				this.addFriend(friendId);
			} else if (e.target.classList.contains('decline-btn')) {
				e.stopPropagation();
				const friendId = e.target.closest('.friend-result').dataset.id;
				this.deleteFriendRequest(friendId);
			} else {
				navigateTo(`/profile/${e.target.closest('.friend-result').dataset?.id}`);
			}
		});
	}

	appendEventlistenters() {
		this.searchInputLister();
		this.searchResultListener();
	}
}
