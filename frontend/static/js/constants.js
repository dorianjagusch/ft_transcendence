const baseURL = 'http://127.0.0.1:8080/';
const userURL = `${baseURL}users/`;
const loginURL = `${baseURL}login/`;
const leaderboardURL = `${baseURL}leaderboards/`;
const settingsURL = `${baseURL}settings/`;
const friendURL = `${baseURL}friends/`;


const problemWithFetchMsg = "There was a problem with the fetch operation: ";

const FRIENDSHIPSTATUS = {
	FRIEND: 'friend',
	NOTFRIEND: 'not-friend',
	PENDINGSENT: 'pending-sent',
	PENDINGRECEIVED: 'pending-received'
};

export default {
	baseURL,
	userURL,
	loginURL,
	leaderboardURL,
	settingsURL,
	friendURL,
	FRIENDSHIPSTATUS
};
