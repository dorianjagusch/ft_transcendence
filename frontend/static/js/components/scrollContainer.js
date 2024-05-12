const scrollContainer = (elements, callback, orientation = 'row') => {

	if (!elements) {
		return;
	}

	const outerScroller = document.createElement('section');
	outerScroller.classList.add('scroll-container');

	const innerScroller = document.createElement('div');
	innerScroller.classList.add('snaps-inline', `${orientation}-scroll`);

	elements.forEach((element) => {
		const currentCard = callback(element);
		currentCard.classList.add('scroll-element');
		innerScroller.appendChild(currentCard);
	});

	outerScroller.appendChild(innerScroller);

	return outerScroller;
};

export { scrollContainer };
