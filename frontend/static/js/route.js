import landingPage from './views/landingView.js';
import loginPage from './views/loginView.js';
import logoutPage from './views/logoutView.js';
import registerPage from './views/registerView.js';
import dashboardPage from './views/dashboardView.js';
import friendsPage from './views/friendsView.js';
import profilePage from './views/profileView.js';
import playPage from './views/playView.js';
import pongPage from './views/pongView.js';
import leaderBoard from './views/leaderboardView.js';
import show404Page from './views/404View.js';
import matchPage from './views/matchView.js';
import previewPage from './views/previewMatchView.js';
import winnerPage from './views/winnerPage.js';

export default [
	{ path: '/404', view: show404Page },
	{ path: '/', view: landingPage },
	{ path: '/login', view: loginPage },
	{ path: '/logout', view: logoutPage },
	{ path: '/register', view: registerPage },
	{ path: '/dashboard', view: dashboardPage },
	{ path: '/friends', view: friendsPage },
	{ path: '/play', view: playPage },
	{ path: '/pong', view: pongPage },
	{ path: '/pong/tournaments/:tournament_id/matches/:match_id', view: pongPage },
	{ path: '/leaderboard', view: leaderBoard },
	{ path: '/profile/:id', view: profilePage },
	{ path: '/match', view: matchPage},
	{ path: '/preview/:tournament_id/matches/:match_id', view: previewPage},
	{ path: '/winner/match/:match_id', view: winnerPage},
	{ path: '/winner/tournament/:tournament_id', view: winnerPage},
];