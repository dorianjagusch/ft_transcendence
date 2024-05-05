
const friendCard = ({username, status, img}) => {

  const friendCard = document.createElement('button');
  friendCard.className = 'scroll-element user-card';

  const imgElement = document.createElement('img');
  imgElement.src = img;

  const userCardText = document.createElement('div');
  userCardText.className = 'user-card-text';

  const userName = document.createElement('div');
  userName.className = 'user-name';
  userName.innerText = username;

  const userStatus = document.createElement('div');
  userStatus.className = 'status';
  userStatus.setAttribute('data-status', status);

  userCardText.appendChild(userName);
  userCardText.appendChild(userStatus);

  friendCard.appendChild(imgElement);
  friendCard.appendChild(userCardText);
  return friendCard;
}

export { friendCard }