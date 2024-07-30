const convertDurationToSeconds = (duration) => {
	const [hours, minutes, seconds] = duration.split(':');
	const totalSeconds = parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseFloat(seconds);
	return totalSeconds;
}

export default convertDurationToSeconds;