from enum import unique
from functools import partial
from urllib.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from django.db.models import Q

from .models import Friends
from .serializers import FriendsSerializer

# rm later
import sys

class FriendsListView(APIView):
    def get(self, request):
        friends = Friends.objects.all()
        serializer = FriendsSerializer(friends, many=True)
        return JsonResponse({"friends" : serializer.data})
    
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


class UserFriendsListView(APIView):
    def get(self,request, user_id):
        friends = Friends.objects.filter(user_id=user_id)
        if friends.exists():
            serializer = FriendsSerializer(friends, many=True)
            return JsonResponse({"friends" : serializer.data})
        else:
            return Response({"message": "No friends found for user"}, status=status.HTTP_404_NOT_FOUND)


class UserApprovedFriendsListView(APIView):
    def get(self, request, user_id):
        user_friendships_sent = Friends.objects.filter(user_id=user_id)
        user_friendships_received = Friends.objects.filter(friend_id=user_id)
        mutual_friendships = user_friendships_sent.filter(friend_id__in=user_friendships_received.values('user_id'))
        
        if mutual_friendships.exists():
            serializer = FriendsSerializer(mutual_friendships, many=True)
            return JsonResponse({"approved friends" : serializer.data})
        else:
            return Response({"message": "No approved friends found for user"}, status=status.HTTP_404_NOT_FOUND)


class UserPendingFriendsListView(APIView):
    def get(self, request, user_id):
        user_friendships_sent = Friends.objects.filter(user_id=user_id)
        user_friendships_received = Friends.objects.filter(friend_id=user_id)
        pending_friendships = user_friendships_sent.exclude(friend_id__in=user_friendships_received.values('user_id'))

        if pending_friendships.exists():
            serializer = FriendsSerializer(pending_friendships, many=True)
            return JsonResponse({"pending friendship requests" : serializer.data})
        else:
            return Response({"message": "No pending friendship requests found for user"}, status=status.HTTP_404_NOT_FOUND)


class UserReceivedFriendsListView(APIView):
    def get(self, request, user_id):
        user_friendships_sent = Friends.objects.filter(user_id=user_id)
        user_friendships_received = Friends.objects.filter(friend_id=user_id)
        received_friendships = user_friendships_received.exclude(user_id__in=user_friendships_sent.values('friend_id'))

        if received_friendships.exists():
            serializer = FriendsSerializer(received_friendships, many=True)
            return JsonResponse({"received friendship requests" : serializer.data})
        else:
            return Response({"message": "No received friendship requests found for user"}, status=status.HTTP_404_NOT_FOUND)

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



    
