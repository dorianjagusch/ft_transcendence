from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from UserManagement.models import User
from .models import Friends
from .serializers import FriendsSerializer


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
    

class FriendsDetailView(APIView):
    def get(self, request, user_id, friend_id):
        try:
            friends = Friends.objects.get(user_id=user_id, friend_id=friend_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FriendsSerializer(friends)
        return Response(serializer.data)
    
    # post only for creating new Friends
    def post(self, request, user_id, friend_id):
        try:
            friends = Friends.objects.get(user_id=user_id, friend_id=friend_id)
            return Response({"message": "Friendship already exists"}, status=status.HTTP_409_CONFLICT)
        except Friends.DoesNotExist:
            if not User.objects.filter(pk=user_id).exists() or not User.objects.filter(pk=friend_id).exists():
                return Response({"message": "User or friend not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = FriendsSerializer(data={'user_id': user_id, 'friend_id': friend_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, user_id, friend_id):
        try:
            friends = Friends.objects.get(user_id=user_id, friend_id=friend_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        friends.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
