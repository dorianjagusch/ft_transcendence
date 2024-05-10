import landingPage from './pages/landingPage.js';
import loginPage from './pages/loginPage.js';
import registerPage from './pages/registerPage.js';
import friendsPage from './pages/friendsPage.js';
import friendPage from './pages/friendPage.js';
import playPage from './pages/playPage.js';
import pongPage from './pages/pongPage.js';
import leaderBoard from './pages/leaderboardPage.js';
import show404Page from './pages/404Page.js';

export default [
	{ path: '/404', view: show404Page },
	{ path: '/', view: landingPage },
	{ path: '/login', view: loginPage },
	{ path: '/register', view: registerPage },
	{ path: '/friends', view: friendsPage },
	{ path: '/play', view: playPage },
	{ path: '/pong', view: pongPage },
	{ path: '/leaderboard', view: leaderBoard },
	{ path: '/friends/:id', view: friendPage },
];
