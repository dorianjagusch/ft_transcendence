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
    def post(self, request):
        serializer = FriendsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            friends = Friends.objects.get(user_id=serializer.data.get('user_id'), friend_id=serializer.data.get('friend_id'))
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        response_serializer = FriendsSerializer(friends)
        return Response(response_serializer.data)


class FriendsDetailView(APIView):
    
    # post only for creating new Friends
    def post(self, request):
        serializer = FriendsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print("user_id of serializer [DATA]: ", serializer.data.get('user_id'), file=sys.stderr)
        # print("user_id of serializer [VALIDATED_DATA]: ", serializer.validated_data.get('user_id'), file=sys.stderr)
        # print("friend_id of serializer: ", serializer.data.get('friend_id'), file=sys.stderr)
        
        # user_id = serializer.data.get('user_id')
        
        # friend_id = serializer.data.get('friend_id')
        # # if not User.objects.filter(pk=friend_id).exists():
        # #     return Response({"message": "user with the id of friend_id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request):

        # is_valid causes an error here because of the 'unique_user_friend_pair' constrait; try to solve later
        # serializer = FriendsSerializer(data=request.data, partial=True)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # user_id = serializer.data.get('user_id')
        # friend_id = serializer.data.get('friend_id')

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


    
