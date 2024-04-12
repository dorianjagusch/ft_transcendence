from django.contrib import admin

# add app models here
from UserManagement.models import User

admin.site.register(User)
