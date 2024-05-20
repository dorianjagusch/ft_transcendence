const user = {
	id: 1,
	username: 'Username',
	img: './static/assets/img/default-user.png',
	description:
		'Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet, aliquid! Reiciendis nobis, dolores optio eaque tempora debitis nulla vel magnam nam soluta quas doloribus sit odit eligendi architecto distinctio voluptas recusandae quos necessitatibus tenetur nisi po',
};

const statObj1 = {
	game: 'Pong',
	stats: {
		highscore: 100,
		gamesPlayed: 10,
		gamesWon: 5,
	},
};
const statObj2 = {
	game: 'Game2',
	stats: {
		highscore: 100,
		gamesPlayed: 10,
		gamesWon: 5,
	},
};

const statObj3 = {
	game: 'Game3',
	stats: {
		highscore: 100,
		gamesPlayed: 10,
		gamesWon: 5,
	},
};

const placementObj1 = {
	game: 'Pong',
	place: 1,
};

const placementObj2 = {
	game: 'Game2',
	place: 101,
};

const historyObj1 = {
	game: 'Pong',
	date: '2021-01-01',
	score: 100,
};
const historyObj2 = {
	game: 'Pong',
	date: '2021-01-02',
	score: 100,
};
const historyObj3 = {
	game: 'Game2',
	date: '2021-01-03',
	score: 100,
};
const historyObj4 = {
	game: 'Pong',
	date: '2021-01-04',
	score: 100,
};
const historyObj5 = {
	game: 'Game2',
	date: '2021-01-05',
	score: 100,
};

const userData = {
	user,
	friendship: 'friend', // | "friend" | "not-friend" | "pending-sent" | "pending-received"
	placements: [
		//[placementObj, ...] | null
		placementObj1,
		placementObj2,
	],
	stats: [
		// [statObj, ...] | null
		statObj1,
		statObj2,
		statObj3,
	],
	playHistory: [
		//[historyObj, ...] | null
		historyObj1,
		historyObj2,
		historyObj3,
		historyObj4,
		historyObj5,
	],
};

export default userData;