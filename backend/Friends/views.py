from enum import unique
from functools import partial
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json

from .models import Friends
from .serializers import FriendsSerializer

class FriendsListView(APIView):
    def get(self, request):
        json_objects = [
            {"id": 2, "username": "hoijjaa"},
            {"id": 3, "username": "hello"},
            # Add more JSON objects as needed
        ]

        # Serialize the list of dictionaries to a JSON string
        json_string = json.dumps(json_objects)
        return JsonResponse(json_string, safe=False)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "User is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        if request.user.id != request.data.get('user_id'):
            return Response({"message": "Cannot access other user's data"},status=status.HTTP_403_FORBIDDEN)
        serializer = FriendsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "User is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        if request.user.id != request.data.get('user_id'):
            return Response({"message": "Cannot access other user's data"},status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')

        try:
            friends = Friends.objects.get(user_id=user_id, friend_id=friend_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"},status=status.HTTP_404_NOT_FOUND)

        # remove possible opposing friend row from Friends table
        try:
            opposing_friends = Friends.objects.get(user_id=friend_id, friend_id=user_id)
            opposing_friends.delete()
        except Friends.DoesNotExist:
            pass

        friends.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# for viewing a single, existing friendship
class FriendshipDetailView(APIView):
    def get(self, request, friendship_id):
        try:
            friends = Friends.objects.get(id=friendship_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        response_serializer = FriendsSerializer(friends)
        return Response(response_serializer.data)

    def delete(self, request, friendship_id):
        try:
            friends = Friends.objects.get(id=friendship_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"},status=status.HTTP_404_NOT_FOUND)

        # remove possible reciprocal friend row from Friends table
        user_id = friends.user_id
        friend_id = friends.friend_id

        try:
            reciprocal_friends = Friends.objects.get(user_id=friend_id, friend_id=user_id)
            reciprocal_friends.delete()
        except Friends.DoesNotExist:
            pass

        friends.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
