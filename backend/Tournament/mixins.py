from User.models import User

class ChangeDeletedUserTournamentNamesMixin:
	"""
    Mixin that changes a user's tournamentplayers' display names to deleted_user.
	Use only when deleting a user.
    """
	def change_tournament_player_names_to_deleted(self, user: User) -> None:
		tournament_players = user.tournament_players.all()
		for player in tournament_players:
			player.display_name = "deleted_user"
			player.save()
