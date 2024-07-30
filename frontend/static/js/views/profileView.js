import AView from './AView.js';
import buttonBar from '../components/profileComponents/buttonBar.js';
import profileImg from '../components/profileComponents/profileImg.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profilePlayHistory from '../components/profileComponents/profilePlayHistory.js';
import constants from '../constants.js';
import {scrollContainer} from '../components/scrollContainer.js';
import UserService from '../services/userService.js';
import FriendService from '../services/friendService.js';
import MatchService from '../services/matchService.js';
import getProfilePicture from '../components/profilePicture.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.userService = new UserService();
		this.friendService = new FriendService();
		this.matchService = new MatchService();
		this.acceptHandler = this.acceptHandler.bind(this);
		this.removeHandler = this.removeHandler.bind(this);
		this.declineHandler = this.declineHandler.bind(this);
		this.selectButtons = this.selectButtons.bind(this);
		this.friendId = params.id;
	}

	selectButtons(relationship) {
		switch (relationship) {
			case constants.FRIENDSHIPSTATUS.FRIEND:
				return [
					{
						className: 'decline-btn',
						textContent: 'Remove friend',
						handler: this.removeHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.NOTFRIEND:
				return [
					{
						className: 'accept-btn',
						textContent: 'Add Friend',
						handler: this.acceptHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGSENT:
				return [
					{
						className: 'decline-btn',
						textContent: 'Cancel Request',
						handler: this.declineHandler,
					},
				];
			case constants.FRIENDSHIPSTATUS.PENDINGRECEIVED:
				return [
					{
						className: 'decline-btn',
						textContent: 'Decline',
						handler: this.declineHandler,
					},
					{
						className: 'accept-btn',
						textContent: 'Accept',
						handler: this.acceptHandler,
					},
				];
			default:
				return null;
		}
	}

	async acceptHandler() {
		const data = {
			friend_id: this.friendId,
		};

		try {
			await this.friendService.postRequest(data);
			super.notify('Friendship created successfully.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	async removeHandler() {
		try {
			await this.friendService.deleteRequest(this.friendId);
			super.notify('Friendship deleted.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error);
		}
	}

	async declineHandler() {
		try {
			await this.friendService.deleteRequest(this.friendId);
			super.notify('Friendship declined successfully.');
			super.navigateTo(`/profile/${this.friendId}`);
		} catch (error) {
			super.notify(error.message, 'error');
		}
	}

	async getOpponent(players) {
		let opponent = players.find((player) => player.user != this.friendId);
		if (!opponent) {
			opponent = {};
			opponent.username = 'AI';
		} else {
			try {
				const opponentData = await this.userService.getRequest(opponent.user);
				opponent.username = opponentData.username;
			} catch (error) {
				opponent.username = 'Deleted User';
			}
		}
		return opponent;
	}

	async getFinishedMatches() {
		const allMatches = await this.matchService.getHistoryMatches(this.friendId);
		const finishedMatches = allMatches.filter(
			(match) => match.state === constants.MATCHSTATUS.FINISHED
		);
		const matchData = await Promise.all(
			finishedMatches.map(async (match) => {
				const players = await this.matchService.getMatchPlayers(match.id);
				const matchDetails = await this.matchService.getMatchDetails(match.id);
				const opponent = await this.getOpponent(players, matchDetails);
				const self = players.find((player) => player.user == this.friendId);
				return {
					match_id: match.id,
					opponent: opponent.username,
					winner: matchDetails.winner,
					loser: matchDetails.loser,
					scoreSelf: self.score,
					scoreOpponent: opponent.username === 'AI' ? 'XX' : opponent.score,
					date: match.start_ts,
					duration: matchDetails.duration,
					ball_contacts: matchDetails.ball_contacts,
					ball_max_speed: matchDetails.ball_max_contacts,
				};
			})
		);
		return matchData;
	}

	async getHTML() {
		let userResponse;
		try {
			userResponse = await this.userService.getRequest(this.friendId);
			userResponse.img = await getProfilePicture(this.friendId);
		} catch (error) {
			this.notify(error.message, 'error');
			this.navigateTo('/friends');
		}

		let history;
		try {
			history = await this.getFinishedMatches();
		} catch (error) {
			history = [];
		}

		const friendship = userResponse.friendship;
		const main = document.querySelector('main');
		main.classList.add('profile', friendship);
		this.setTitle(`${userResponse.username}'s Profile`);
		const userName = profileTitle(userResponse.username);
		const userImg = profileImg(userResponse.img);

		const buttons = this.selectButtons(friendship);
		const actionBar = buttonBar(buttons);

		const userHistory = scrollContainer(history, profilePlayHistory, 'col', 'history-list')
		userHistory?.classList.add('play-history');

		this.updateMain(userName, userImg, actionBar, userHistory);
	}
}
