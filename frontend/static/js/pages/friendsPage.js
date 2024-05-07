import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Friends Page');
	}

	async getHTML() {
		const friends = [
			{
				id: 1,
				username: 'user1',
				img: 'https://unsplash.it/150',
			},
			{
				id: 2,
				username: 'user2',
				img: 'https://unsplash.it/150',
			},
			{
				id: 3,
				username: 'user3',
				img: 'https://unsplash.it/150',
			},
			{
				id: 4,
				username: 'user4',
				img: 'https://unsplash.it/150',
			},
			{
				id: 5,
				username: 'user5',
				img: 'https://unsplash.it/150',
			},
			{
				id: 6,
				username: 'user6',
				img: 'https://unsplash.it/150',
			},
			{
				id: 7,
				username: 'user7',
				img: 'https://unsplash.it/150',
			},
			{
				id: 8,
				username: 'user8',
				img: 'https://unsplash.it/150',
			},
			{
				id: 9,
				username: 'user9',
				img: 'https://unsplash.it/150',
			},
			{
				id: 10,
				username: 'user10',
				img: 'https://unsplash.it/150',
			},
			{
				id: 11,
				username: 'user11',
				img: 'https://unsplash.it/150',
			},
			{
				id: 12,
				username: 'user12',
				img: 'https://unsplash.it/150',
			},
			{
				id: 13,
				username: 'user13',
				img: 'https://unsplash.it/150',
			},
		];

		const friendScroller = scrollContainer(friends, friendCard);
		friendScroller.classList.add('friends', 'bg-secondary');

		const requestScroller = scrollContainer(friends, requestCard);
		requestScroller.classList.add('friend-request', 'bg-secondary');

		this.updateMain(friendScroller, requestScroller);
	}
}
