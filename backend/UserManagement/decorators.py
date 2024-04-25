from functools import wraps
from django.http import HttpResponseForbidden

def user_is_object_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Check if the user is logged in
        if not self.request.user.is_authenticated:
            # Redirect or return an error response for unauthenticated users
            return HttpResponseForbidden("You must be logged in to access this resource.")

        # Check if the user is the owner of the object being modified
        object_owner_id = kwargs.get('user_id')  # Assuming the user_id is passed as a URL parameter
        if self.request.user.id != object_owner_id:
            # Redirect or return an error response for unauthorized users
            return HttpResponseForbidden("You are not authorized to modify this resource.")

        # Call the original view function if the checks pass
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
