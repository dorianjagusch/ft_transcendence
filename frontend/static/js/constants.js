const protocol = 'http://';
const location = 'localhost:8080/';
const baseURL = `${protocol}${location}`;
const userURL = `${baseURL}users/`;
const loginURL = `${baseURL}login/`;
const logoutURL = `${baseURL}logout/`;
const leaderboardURL = `${baseURL}leaderboards/`;
const settingsURL = `${baseURL}settings/`;
const friendURL = `${baseURL}friends/`;
const pongURL = `${baseURL}match/`;
const authenticationURL = `${baseURL}tokens/`;
const tournamentURL = `${baseURL}tournaments/`;

const allowedPaths = ['/login', '/register', '/', '/pong'];

const problemWithFetchMsg = 'There was a problem with the fetch operation: ';

const FRIENDSHIPSTATUS = {
	FRIEND: 'friend',
	NOTFRIEND: 'not-friend',
	PENDINGSENT: 'pending-sent',
	PENDINGRECEIVED: 'pending-received',
};

const MATCHSTATUS = {
	LOBBY: 'lobby',
	IN_PROGRESS: 'in_progress',
	FINISHED: 'finished',
	ABORTED: 'aborted',
};

const GAMES = {
	Pong: 0,
};

export default {
	protocol,
	location,
	baseURL,
	userURL,
	loginURL,
	logoutURL,
	leaderboardURL,
	settingsURL,
	friendURL,
	pongURL,
	authenticationURL,
	tournamentURL,
	allowedPaths,
	FRIENDSHIPSTATUS,
	MATCHSTATUS,
	problemWithFetchMsg,
	GAMES,
};
