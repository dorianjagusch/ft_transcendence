import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';


const main = document.querySelector('main');




const showFriends = async () => {

	const friends = [
    {
      username: "test",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test1",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test2",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test3",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test4",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test5",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
    {
      username: "test6",
      img: "https://unsplash.it/200/200",
	  status: "online",
    },
  ];
	// const friends = Call friendsAPI	to	get	friends in a json array

	friendScroller.classList.add('scroll-container', 'friends', 'bg-secondary');
	
  const friendScroller = document.createElement('section');
  friendScroller.classList.add('scroll-container', 'friends', 'bg-secondary');

  const friendInnerScroller = document.createElement('div');
  friendInnerScroller.classList.add('snaps-inline', 'row-scroll');

	friends.forEach((friend) => {
		const currentCard = friendCard(friend);
		currentCard.classList.add('scroll-element', 'user-card');
		friendInnerScroller.appendChild(currentCard);
	});

	friendScroller.appendChild(friendInnerScroller);

	main.appendChild(friendScroller);
}

export default showFriends;