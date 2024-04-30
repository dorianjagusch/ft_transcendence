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

# add app views here
<<<<<<< HEAD
from UserManagement.views import UserDetailView, \
                                UserListView

from Friends.views import  FriendsListAllView, \
                        FriendsListView, \
                        FriendsSingleFriendshipView, \
                        FriendsDetailView
=======
from User.views import UserDetailView, \
                        UserListView, \
                        UserLoginView, \
                        UserAdminDetailsView
>>>>>>> e381115527ae0494cd16789ea7d912c43ef1cb2d

urlpatterns = [
	path('admin/', admin.site.urls),

	# User views
	path('users/', UserListView.as_view()),
<<<<<<< HEAD
	path('users/<int:id>', UserDetailView.as_view()),

    # Friends views
    path('friends/all', FriendsListAllView.as_view()), # for debugging, will be removed later
    path('<int:user_id>/friends', FriendsListView.as_view()),
    path('<int:user_id>/friends/<int:friend_id>', FriendsSingleFriendshipView.as_view()),
    path('friends/', FriendsDetailView.as_view()),
=======
	path('users/<int:user_id>', UserDetailView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('admins/', UserAdminDetailsView.as_view()),
>>>>>>> e381115527ae0494cd16789ea7d912c43ef1cb2d

]
