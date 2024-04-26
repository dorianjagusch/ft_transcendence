import json
from functools import wraps
from django.http import HttpResponseForbidden

from .models import User

def user_is_object_owner_url(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not self.request.user.is_authenticated:
            # Redirect or return an error response for unauthenticated users
            return HttpResponseForbidden("You must be logged in to access this resource.")
        
        # Allow superusers to bypass the ownership check
        if self.request.user.is_superuser:
            return view_func(self, request, *args, **kwargs)

        # Check if the user is the owner of the object being modified
        object_owner_id = kwargs.get('user_id')  # Assuming the user_id is passed as a URL parameter
        if self.request.user.id != object_owner_id:
            # Redirect or return an error response for unauthorized users
            return HttpResponseForbidden("You are not authorized to modify this resource.")

        # Call the original view function if the checks pass
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view


# FOR LATER, TALK WITH MERI

def user_is_object_owner_body(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")
        
        if self.request.user.is_superuser:
            return view_func(self, request, *args, **kwargs)

        # Get the JSON body from the request
        try:
            body = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseForbidden("Invalid JSON body.")

        # Retrieve the user object based on the provided 'id' or 'username'
        user = None
        if 'id' in body:
            user_id = body['id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponseForbidden("User does not exist.")
            if 'username' in body and body['username'] != user.username:
                return HttpResponseForbidden("Username in the body does not match the user.")
        elif 'username' in body:
            username = body['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponseForbidden("User does not exist.")

        # Check if the user is the owner of the object being modified
        if user and self.request.user.id != user.id:
            return HttpResponseForbidden("You are not authorized to modify this resource.")

        # Call the original view function if the checks pass
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view


def user_is_object_owner_url_and_body(view_func):
    return user_is_object_owner_body(user_is_object_owner_url(view_func))