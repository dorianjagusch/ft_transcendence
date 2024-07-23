from django.shortcuts import render
from rest_framework.views import APIView
from .mixins import LeaderBoardTableMixin

class LeaderboardListView(APIView, LeaderBoardTableMixin):    
	def get(self, request):
		return self.leader_table_response()
