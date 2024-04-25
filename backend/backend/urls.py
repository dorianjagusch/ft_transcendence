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
# from UserManagement.views import UserDetailView
# from UserManagement.views import UserListView

# from UserManagement.views import UserLoginView

from User.views import UserDetailView, \
                        UserListView, \
                        UserLoginView

urlpatterns = [
	path('admin/', admin.site.urls),

	# UserManagement views
	path('users/', UserListView.as_view()),
	path('users/<int:user_id>', UserDetailView.as_view()),

    path('users/login/', UserLoginView.as_view()),
]
