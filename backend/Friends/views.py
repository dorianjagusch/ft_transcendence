from enum import unique
from functools import partial
from urllib.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from UserManagement.models import User
from .models import Friends
from .serializers import FriendsSerializer

# rm later
import sys

class FriendsListAllView(APIView):
    def get(self, request):
        friends = Friends.objects.all()
        serializer = FriendsSerializer(friends, many=True)
        return JsonResponse({"friends" : serializer.data})

class FriendsListView(APIView):
    def get(self,request, user_id):
        friends = Friends.objects.filter(user_id=user_id)
        if friends.exists():
            serializer = FriendsSerializer(friends, many=True)
            return JsonResponse({"friends" : serializer.data})
        else:
            return Response({"message": "No friends found for user"}, status=status.HTTP_404_NOT_FOUND)

# for viewing a single, existing friendship
class FriendsSingleFriendshipView(APIView):
    def get(self, request, user_id, friend_id):
        try:
            friends = Friends.objects.get(user_id=user_id, friend_id=friend_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        response_serializer = FriendsSerializer(friends)
        return Response(response_serializer.data)


class FriendsDetailView(APIView):
    def post(self, request):
        serializer = FriendsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request):
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


    
