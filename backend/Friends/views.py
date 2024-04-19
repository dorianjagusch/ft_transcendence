from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .models import Friends
from .serializers import FriendsSerializer


class FriendsListAllView(APIView):
    def get(self, request):
        friends = Friends.objects.all()
        serializer = FriendsSerializer(friends, many=True)
        return JsonResponse({"all Friends" : serializer.data})

class FriendsListView(APIView):
    def get(self,request, user_id):
        friends = Friends.objects.filter(user1_id=user_id)
        if friends.exists():
            serializer = FriendsSerializer(friends, many=True)
            return JsonResponse({"user Friends" : serializer.data})
        else:
            return Response({"message": "No friends found for user"}, status=status.HTTP_404_NOT_FOUND)
    

class FriendsDetailView(APIView):
    def get(self, request, current_user_id, friends_user_id):
        try:
            friends = Friends.objects.get(user1_id=current_user_id, user2_id=friends_user_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FriendsSerializer(friends)
        return Response(serializer.data)
    
    # post only for creating new Friends
    def post(self, request, current_user_id, friends_user_id):
        try:
            friends = Friends.objects.get(user1_id=current_user_id, user2_id=friends_user_id)
            return Response({"message": "Friendship already exists"}, status=status.HTTP_409_CONFLICT)
        except Friends.DoesNotExist:
            serializer = FriendsSerializer(data={'user1_id': current_user_id, 'user2_id': friends_user_id})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, current_user_id, friends_user_id):
        try:
            friends = Friends.objects.get(user1_id=current_user_id, user2_id=friends_user_id)
        except Friends.DoesNotExist:
            return Response({"message": "Friendship doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        friends.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
