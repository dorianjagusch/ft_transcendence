# import json
# from functools import wraps
# from django.http import HttpResponseForbidden
# from rest_framework import serializers, status
# from rest_framework.response import Response

# # rm later
# import sys

# def must_be_authenticated(view_func):
#     @wraps(view_func)
#     def _wrapped_view(self, request, *args, **kwargs):
#         print("in DECORATOR must_be_authenticated", file=sys.stderr)

#         if not self.request.user.is_authenticated:
#             return HttpResponseForbidden("You must be logged in to access this resource.")

#         # Call the original view function if the checks pass
#         return view_func(self, request, *args, **kwargs)
#     return _wrapped_view


# def must_be_url_user(view_func):
#     @wraps(view_func)
#     def _wrapped_view(self, request, *args, **kwargs):

#         print("in DECORATOR must_be_url_user", file=sys.stderr)
    
#         # Allow superusers to bypass the ownership check
#         if self.request.user.is_superuser:
#             return view_func(self, request, *args, **kwargs)

#         object_owner_id = kwargs.get('user_id')  # URL parameter
#         if self.request.user.id != object_owner_id:

#             return HttpResponseForbidden("You are not authorized to modify this resource.")

#         # Call the original view function if the checks pass
#         return view_func(self, request, *args, **kwargs)

#     return must_be_authenticated(_wrapped_view)


# def must_be_body_user_id(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):

#         print("in DECORATOR must_be_body_user_id", file=sys.stderr)

#         try:
#             body_data = json.loads(request.body)
#             user_id = body_data.get('user_id')
#         except json.JSONDecodeError:
#             return HttpResponseForbidden("Invalid JSON data provided.")
#         except KeyError:
#             return HttpResponseForbidden("Missing 'user_id' in JSON data.")

#         if not user_id:
#             return HttpResponseForbidden("No 'user_id' provided in JSON data.")

# 		# Allow superusers to bypass the ownership check
#         if request.user.is_superuser:
#             return view_func(request, *args, **kwargs)

#         if request.user.id != user_id:
#             return HttpResponseForbidden("You are not authorized to modify this resource.")

#         return view_func(request, *args, **kwargs)
#     return must_be_authenticated(_wrapped_view)


# def valid_serializer_in_body(serializer_class, **kwargs):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):

#             print("in DECORATOR valid_serializer_in_body", file=sys.stderr)

#             serialized_data = request.data
#             serializer = serializer_class(data=serialized_data, **kwargs)
#             try:
#                 serializer.is_valid(raise_exception=True)
#                 return view_func(request, *args, **kwargs)
#             except serializers.ValidationError as e:
#                 return Response({'message': "Non-valid JSON object in request body.",'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
#         return _wrapped_view
#     return decorator

# class method_decorator_chain:
#     def __init__(self, *decorators):
#         self.decorators = decorators

#     def __call__(self, view_func):
#         for decorator in reversed(self.decorators):
#             view_func = decorator(view_func)
#         return view_func

import json
from functools import wraps
from django.http import HttpResponseForbidden
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework.views import APIView

from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

# rm later
import sys

def must_be_authenticated(view_func):
    # print("\tDECORATOR must_be_authenticated", file=sys.stderr)
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = args[0] if args else None
        print("in DECORATOR must_be_authenticated", file=sys.stderr)

        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to access this resource.")

        # Call the original view function if the checks pass
        return view_func(*args, **kwargs)
    return _wrapped_view


def must_be_url_user(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = args[0] if args else None

        print("in DECORATOR must_be_url_user", file=sys.stderr)
    
        # Allow superusers to bypass the ownership check
        if request.user.is_superuser:
            return view_func(*args, **kwargs)

        object_owner_id = kwargs.get('user_id')  # URL parameter
        if request.user.id != object_owner_id:

            return HttpResponseForbidden("You are not authorized to modify this resource.")

        # Call the original view function if the checks pass
        return view_func(*args, **kwargs)
    return must_be_authenticated(_wrapped_view)


def must_be_body_user_id(view_func):
    # print("\tDECORATOR must_be_body_user_id", file=sys.stderr)
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = args[0] if args else None

        print("in DECORATOR must_be_body_user_id", file=sys.stderr)

        try:
            body_data = json.loads(request.body)
            user_id = body_data.get('user_id')
        except json.JSONDecodeError:
            return HttpResponseForbidden("Invalid JSON data provided.")
        except KeyError:
            return HttpResponseForbidden("Missing 'user_id' in JSON data.")

        if not user_id:
            return HttpResponseForbidden("No 'user_id' provided in JSON data.")

		# Allow superusers to bypass the ownership check
        if request.user.is_superuser:
            return view_func(*args, **kwargs)

        if request.user.id != user_id:
            return HttpResponseForbidden("You are not authorized to modify this resource.")
        
        print("X", file=sys.stderr)


        return view_func(*args, **kwargs)
    return must_be_authenticated(_wrapped_view)


def valid_serializer_in_body(serializer_class, **kwargs):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            request = args[0] if args else None

            print("in DECORATOR valid_serializer_in_body", file=sys.stderr)

           # Dynamically create a subclass of the serializer that ignores unique and unique together constraints
            class IgnoringUniqueConstraintsSerializer(serializer_class):
                
                print("IgnoringUniqueConstraintsSerializer", file=sys.stderr)

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                    self.remove_unique_validators()

                def remove_unique_validators(self):
                    # Remove UniqueValidator from the field validators
                    for field_name, field in self.fields.items():
                        field.validators = [v for v in field.validators if not isinstance(v, UniqueValidator)]

                    # Remove UniqueTogetherValidator from the serializer validators
                    self.validators = [v for v in self.validators if not isinstance(v, UniqueTogetherValidator)]


            serialized_data = request.data
            serializer = IgnoringUniqueConstraintsSerializer(data=serialized_data, **kwargs)
            try:
                serializer.is_valid(raise_exception=True)
                return view_func(*args, **kwargs)
            except serializers.ValidationError as e:
                return Response({'message': "Non-valid JSON object in request body.",'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return _wrapped_view
    return decorator

    
