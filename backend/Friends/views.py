from enum import unique
from functools import partial
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.serializers import UserOutputSerializer
from .models import Friends
from .serializers import FriendsSerializer
from .friendShipStatus import FriendShipStatus

class FriendsListView(APIView):
    def get(self, request):
        #if not request.user.is_authenticated:
        #    return Response({"message": "User is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        friendship_status = request.query_params.get('friendship_status')
        if not friendship_status or friendship_status == FriendShipStatus.NONE.value:
            return Response({"message": "Expected to get parameter 'friendship_status'"},status=status.HTTP_400_BAD_REQUEST)
        user_id = 1
        friends = Friends.objects.get_user_friends(user_id, friendship_status)
        serializer = UserOutputSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #if not request.user.is_authenticated:
        #    return Response({"message": "User is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)
        #if request.user.id != request.data.get('user_id'):
        #    return Response({"message": "Cannot access other user's data"},status=status.HTTP_403_FORBIDDEN)
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
