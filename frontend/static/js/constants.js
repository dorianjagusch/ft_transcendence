// const baseURL = 'http://localhost:8080/';
const baseURL = 'http://localhost/';
const userURL = `${baseURL}users/`;
const loginURL = `${baseURL}login/`;
const logoutURL = `${baseURL}logout/`;
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
	logoutURL,
	leaderboardURL,
	settingsURL,
	friendURL,
	FRIENDSHIPSTATUS
};
