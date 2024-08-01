const protocol = 'https://';
const location = 'localhost:8443/';
const baseURL = `${protocol}${location}`;
const userURL = `${baseURL}api/users/`;
const loginURL = `${baseURL}api/login/`;
const logoutURL = `${baseURL}api/logout/`;
const leaderboardURL = `${baseURL}api/leaderboard/`;
const settingsURL = `${baseURL}api/settings/`;
const friendURL = `${baseURL}api/friends/`;
const pongURL = `${baseURL}api/match/`;
const authenticationURL = `${baseURL}api/tokens/`;
const tournamentURL = `${baseURL}api/tournaments/`;
const matchURL = `${baseURL}api/matches/`;
const playerURL = `${baseURL}api/players/`;

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
	matchURL,
	playerURL,
	allowedPaths,
	FRIENDSHIPSTATUS,
	MATCHSTATUS,
	problemWithFetchMsg,
	GAMES,
};
