"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from pong.consumers import PongConsumer

# User views
from User.views import (
    UserDetailView,
    UserListView,
    UserProfilePictureView,
    UserLoginView,
    UserLogoutView,
    UserAdminDetailsView
)

# Friends views
from Friends.views import (
    FriendsListView,
    FriendshipDetailView
)

# Tokens views
from Tokens.views import SingleMatchGuestTokenView

# Match views
from Match.views import (
    MatchView,
    LaunchTestMatchView
)

# Tournament views
from Tournament.views import (
    TournamentListView,
    TournamentDetailView,
    TournamentPlayerListView,
    TournamentPlayerDetailView,
    TournamentMatchListView,
    TournamentMatchDetailView
)

# Stats views
from stats.views import (
    StatsView,
    LeaderBoardView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # User views
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/profile_pictures/', UserProfilePictureView.as_view(), name='user-profile-pictures'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('admins/', UserAdminDetailsView.as_view(), name='user-admin-details'),

    # Friends views
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friends/<int:friend_id>/', FriendshipDetailView.as_view(), name='friendship-detail'),

    # Tokens views
    path('tokens/match/', SingleMatchGuestTokenView.as_view(), name='single-match-guest-token'),

    # Match views
    path('match/', MatchView.as_view(), name='match-list'),
    path('match/test/', LaunchTestMatchView.as_view(), name='launch-test-match'),  # TEMPORARY

    # Tournament views
    path('tournaments/', TournamentListView.as_view(), name='tournament-list'),
    path('tournaments/<int:tournament_id>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('tournaments/<int:tournament_id>/players/', TournamentPlayerListView.as_view(), name='tournament-player-list'),
    path('tournaments/<int:tournament_id>/players/<int:tournamentplayer_id>/', TournamentPlayerDetailView.as_view(), name='tournament-player-detail'),
    path('tournaments/<int:tournament_id>/matches/', TournamentMatchListView.as_view(), name='tournament-match-list'),
    path('tournaments/<int:tournament_id>/matches/<int:tournament_match_id>/', TournamentMatchDetailView.as_view(), name='tournament-match-detail'),

    # Stats views
    path('stats/', StatsView.as_view(), name='stats'),
    path('leaderboard/', LeaderBoardView.as_view(), name='leaderboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# WebSocket URL patterns
websocket_urlpatterns = [
    path('pong/<int:match_id>/', PongConsumer.as_asgi(), name='pong-consumer'),
]
