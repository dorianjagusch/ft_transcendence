import { scrollContainer } from '../components/scrollContainer.js';
import { PlacementCard } from '../components/placementCard.js';
import AView from './AView.js';
import LeaderBoardService from '../services/leaderBoardService.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Leaderboard');
		this.leaderBoardService = new LeaderBoardService();
	}

	async getHTML() {
		// const players = [
		// 	{
		// 		username: 'player1',
		// 		wins: 1000,
		// 		img: 'http://unsplash.it/200',
		// 		place: 1,
		// 	},
		// 	{
		// 		username: 'player2',
		// 		wins: 800,
		// 		img: 'http://unsplash.it/200',
		// 		place: 2,
		// 	},
		// 	{
		// 		username: 'player3',
		// 		wins: 700,
		// 		img: 'http://unsplash.it/200',
		// 		place: 3,
		// 	},
		// 	{
		// 		username: 'player4',
		// 		wins: 600,
		// 		img: 'http://unsplash.it/200',
		// 		place: 4,
		// 	},
		// 	{
		// 		username: 'player5',
		// 		wins: 500,
		// 		img: 'http://unsplash.it/200',
		// 		place: 5,
		// 	},
		// 	{
		// 		username: 'player6',
		// 		wins: 400,
		// 		img: 'http://unsplash.it/200',
		// 		place: 6,
		// 	},
		// 	{
		// 		username: 'player7',
		// 		wins: 300,
		// 		img: 'http://unsplash.it/200',
		// 		place: 7,
		// 	},
		// 	{
		// 		username: 'player8',
		// 		wins: 200,
		// 		img: 'http://unsplash.it/200',
		// 		place: 8,
		// 	},
		// 	{
		// 		username: 'player9',
		// 		wins: 100,
		// 		img: 'http://unsplash.it/200',
		// 		place: 9,
		// 	},
		// 	{
		// 		username: 'player10',
		// 		wins: 90,
		// 		img: 'http://unsplash.it/200',
		// 		place: 10,
		// 	},
		// 	{
		// 		username: 'player11',
		// 		wins: 80,
		// 		img: 'http://unsplash.it/200',
		// 		place: 11,
		// 	},
		// 	{
		// 		username: 'player12',
		// 		wins: 70,
		// 		img: 'http://unsplash.it/200',
		// 		place: 12,
		// 	},
		// 	{
		// 		username: 'player13',
		// 		wins: 60,
		// 		img: 'http://unsplash.it/200',
		// 		place: 13,
		// 	},
		// 	{
		// 		username: 'player14',
		// 		wins: 50,
		// 		img: 'http://unsplash.it/200',
		// 		place: 14,
		// 	},
		// 	{
		// 		username: 'player15',
		// 		wins: 40,
		// 		img: 'http://unsplash.it/200',
		// 		place: 15,
		// 	},
		// 	{
		// 		username: 'player16',
		// 		wins: 30,
		// 		img: 'http://unsplash.it/200',
		// 		place: 16,
		// 	},
		// ];

		// get players from API
		debugger;
		const players = await this.leaderBoardService.getLeaderBoard();

		const leaderBoardOne = scrollContainer(players, PlacementCard, 'column');
		leaderBoardOne.classList.add('leaderboard', 'bg-secondary');
		this.updateMain(leaderBoardOne);


	}
}
