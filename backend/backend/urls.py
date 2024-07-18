"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from pong.consumers import PongConsumer

# add app views here
from User.views import UserDetailView, \
						UserListView, \
						UserProfilePictureView, \
						UserLoginView, \
						UserLogoutView, \
						UserAdminDetailsView

from Friends.views import FriendsListView, \
						FriendshipDetailView

from Tokens.views import SingleMatchGuestTokenView

from Match.views import MatchView, \
							LaunchTestMatchView


from Tournament.views import TournamentListView, \
								TournamentDetailView, \
								TournamentPlayerListView, \
								TournamentPlayerDetailView

from stats.views import StatsView, \
							LeaderBoardView


urlpatterns = [
	path('admin/', admin.site.urls),

	# User views
	path('users/', UserListView.as_view()),
	path('users/<int:user_id>', UserDetailView.as_view()),
	path('users/<int:user_id>/profile_pictures/', UserProfilePictureView.as_view()),
	path('login/', UserLoginView.as_view()),
	path('logout/', UserLogoutView.as_view()),
	path('admins/', UserAdminDetailsView.as_view()),


	# Friends views
	path('friends/', FriendsListView.as_view()),
	path('friends/<int:friend_id>', FriendshipDetailView.as_view()),

	# Tokens views
	path('tokens/match/', SingleMatchGuestTokenView.as_view()),

	# Match Views
	path('match/', MatchView.as_view()),
	path('match/test/', LaunchTestMatchView.as_view()), # TEMPORARY


	# Tournament views
	path('tournaments/', TournamentListView.as_view()),
	path('tournaments/<int:tournament_id>', TournamentDetailView.as_view()),
	path('tournaments/<int:tournament_id>/players/', TournamentPlayerListView.as_view()),
	path('tournaments/<int:tournament_id>/players/<int:tournamentplayer_id>', TournamentPlayerDetailView.as_view()),
]

	# Stats Views
	path('stats/', StatsView.as_view()),
	path('leaderboard/', LeaderBoardView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


websocket_urlpatterns = [
    path('pong/<int:match_id>', PongConsumer.as_asgi()),
]
