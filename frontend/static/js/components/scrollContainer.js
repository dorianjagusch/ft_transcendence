
const scrollContainer = (elements, callback) => {

  const outerScroller = document.createElement('section');
  outerScroller.classList.add('scroll-container');

  const innerScroller = document.createElement('div');
  innerScroller.classList.add('snaps-inline', 'row-scroll');

  elements.forEach((element) => {
    const currentCard = callback(element);
    currentCard.classList.add('scroll-element');
    innerScroller.appendChild(currentCard);
  });

  outerScroller.appendChild(innerScroller);

  return outerScroller;
}

export { scrollContainer }