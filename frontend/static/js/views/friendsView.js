import {friendCard} from '../components/friendCard.js';
import {requestCard} from '../components/requestCard.js';
import {scrollContainer, populateInnerScroller} from '../components/scrollContainer.js';
import SearchFriendsModal from '../components/dialogs/searchFriendsModal.js';
import FriendService from '../services/friendService.js';
import constants from '../constants.js';
import AView from './AView.js';
import getProfilePicture from '../components/profilePicture.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Friends');
		this.friendService = new FriendService();
		this.acceptHandler = this.acceptHandler.bind(this);
		this.declineHandler = this.declineHandler.bind(this);
		this.profileHandler = this.profileHandler.bind(this);
		this.mapResponse = this.mapResponse.bind(this);
		this.populateScroller = this.populateScroller.bind(this);
	}

	profileHandler(friendId) {
		super.navigateTo(`/profile/${friendId}`);
	}

	acceptHandler(friendId) {
		const data = {
			friend_id: friendId,
		};
		try {
			this.friendService.postRequest(data).then(() => {
				super.notify('Friendship created successfully.');
				super.navigateTo('/friends');
			});
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	declineHandler(friendId) {
		try {
			this.friendService.deleteRequest(friendId).then(() => {
				super.notify('Friendship declined successfully.');
				super.navigateTo('/friends');
			});
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	openSearchFriendsmodal() {
		const modal = document.querySelector('.search-friends-modal');
		modal.showModal();
	}

	createScroller(friendsArray, card, tokens, identifier) {
		let scroller = scrollContainer(friendsArray, (friend) => card(friend, this.profileHandler));
		scroller.classList.add(tokens, identifier);
		scroller.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.classList.contains('check-btn')) {
				e.stopPropagation();
				this.acceptHandler(e.target.closest('.scroll-element').dataset.id);
			}
			if (e.target.classList.contains('x-btn')) {
				e.stopPropagation();
				this.declineHandler(e.target.closest('.scroll-element').dataset.id);
			}
			if (e.target.classList.contains('scroll-element')) {
				e.stopPropagation();
				this.profileHandler(e.target.closest('.scroll-element').dataset.id);
			}
		});
		return scroller;
	}

	async mapResponse(response) {
		if (!response){
			return [];
		}
		const promises = response.map(async (element) => {
			try {
				const profileImg = await getProfilePicture(element.id);
				const userData = {
					id: element.id,
					username: element.username,
					status: element.is_online ? 'online' : 'offline',
					img: profileImg,
				};
				return userData;
			} catch (error) {
				notify(error.message, 'error');
				return null;
			}
		});
		return await Promise.all(promises);
	}

	async populateScroller(scrollerSelector, card, statusFilter) {
		const scroller = document.querySelector(`${scrollerSelector} > ul`);
		const data = await this.friendService.getAllRequest(statusFilter);
		const userData = await this.mapResponse(data);
		populateInnerScroller(userData, scroller, card);
	}

	async getHTML() {
		let acceptedFriends = [];
		let pendingFriends = [];
		let friendScroller = this.createScroller(
			acceptedFriends,
			friendCard,
			'friends',
			'bg-secondary'
		);
		let requestScroller = this.createScroller(
			pendingFriends,
			requestCard,
			'friend-request',
			'bg-secondary'
		);

		const friendTitle = document.createElement('h2');
		friendTitle.textContent = 'Friends';
		const requestTitle = document.createElement('h2');
		requestTitle.textContent = 'Friend Requests';

		const searchFriendsSection = document.createElement('section');
		searchFriendsSection.classList.add('search-friends');
		const searchFriendsButton = document.createElement('button');
		searchFriendsButton.classList.add('primary-btn');
		searchFriendsButton.textContent = 'Search Friends';
		searchFriendsSection.appendChild(searchFriendsButton);
		const searchFriendsModal = new SearchFriendsModal();
		searchFriendsModal.dialog.classList.add('search-friends-modal');
		searchFriendsButton.addEventListener('click', () => {
			this.openSearchFriendsmodal();
		});

		this.updateMain(
			friendTitle,
			friendScroller,
			requestTitle,
			requestScroller,
			searchFriendsSection,
			searchFriendsModal.dialog
		);

		try {
			await this.populateScroller('.friends', friendCard, constants.FRIENDSHIPSTATUS.FRIEND);
			await this.populateScroller(
				'.friend-request',
				requestCard,
				constants.FRIENDSHIPSTATUS.PENDINGRECEIVED
			);
		} catch (error) {
			this.notify('An error occured when retrieving your friends', 'error');
		}
	}
}
