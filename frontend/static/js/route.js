import landingPage from './pages/landingPage.js';
import loginPage from './pages/loginPage.js';
import registerPage from './pages/registerPage.js';
import friendsPage from './pages/friendsPage.js';
import profilePage from './pages/profilePage.js';
import playPage from './pages/playPage.js';
import leaderBoard from './pages/leaderboardPage.js';
import show404Page from './pages/404Page.js';

export default [
	{ path: '/404', view: show404Page },
	{ path: '/', view: landingPage },
	{ path: '/login', view: loginPage },
	{ path: '/register', view: registerPage },
	{ path: '/friends', view: friendsPage },
	{ path: '/play', view: playPage },
	{ path: '/leaderboard', view: leaderBoard },
	{ path: '/profile', view: profilePage },
	{ path: '/privacypolicy.html'}
];
