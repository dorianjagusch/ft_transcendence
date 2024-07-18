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


const placementObj1 = {
	game: 'Pong',
	place: 1,
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
	game: 'Pong',
	date: '2021-01-04',
	score: 100,
};

const userData = {
	user,
	placements: [
		//[placementObj, ...] | null
		placementObj1,
	],
	stats: [
		// [statObj, ...] | null
		statObj1,
	],
	playHistory: [
		//[historyObj, ...] | null
		historyObj1,
		historyObj2,
		historyObj3,
	],
};

export default userData