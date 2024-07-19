const scrollContainer = (elements, orientation = 'row', ...classNames) => {

	if (!elements) {
		return;
	}

	const outerScroller = document.createElement('section');
	outerScroller.classList.add('scroll-container');

	const innerScroller = document.createElement('ul');
	innerScroller.classList.add('snaps-inline',
		`${orientation}-scroll`,
		...classNames);

	outerScroller.appendChild(innerScroller);

	return outerScroller;
};

export { scrollContainer };
