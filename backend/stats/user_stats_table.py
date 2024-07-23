class UserTable:
	def __init__(self, user, wins, losses, total_games_played, win_loss_ratio, winning_streak, position_in_leaderboard):
		self.user = user
		self.wins = wins
		self.losses = losses
		self.total_games_played = total_games_played
		self.win_loss_ratio = win_loss_ratio
		self.winning_streak = winning_streak
		self.position_in_leaderboard = position_in_leaderboard