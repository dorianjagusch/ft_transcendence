const ImageButton = (url) => {
	const button = document.createElement('button');
	const image = document.createElement('img');
	image.src = url;
	button.appendChild(image);
	return button;
}

export default ImageButton;
