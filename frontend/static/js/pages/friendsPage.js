import { friendCard } from '../components/friendCard.js';
import { requestCard } from '../components/requestCard.js';
import { scrollContainer } from '../components/scrollContainer.js'

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

  const friendScroller = scrollContainer(friends, friendCard);
	friendScroller.classList.add('friends', 'bg-secondary');

  const requestScroller = scrollContainer(friends, friendCard);
	requestScroller.classList.add('friend-request', 'bg-secondary');


	main.appendChild(friendScroller);
	main.appendChild(requestScroller);
}

export default showFriends;