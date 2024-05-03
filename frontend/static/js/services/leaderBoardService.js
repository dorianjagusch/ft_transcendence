
const getAll = async () => {
	const url = 'http://127.0.0.1:8080/leaderboard';
	const response = await fetch(url);
	if (response.status !== 200) {
		throw new Error('Failed to fetch leaderboard');
	}
	const data = await response.json();
	return data;
}

export default {getAll};