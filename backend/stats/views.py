from django.shortcuts import render
from rest_framework.views import APIView
import plotly.graph_objects as go
import plotly.io as pio
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
# from django.utils.decorators import method_decorator
# from User.serializers import UserOutputSerializer

# from shared_utilities.decorators import must_be_authenticated, \
# 									must_be_body_user_id, \
# 									valid_serializer_in_body

class StatsView(APIView):
	def get(self, request):
		x = [1, 2, 3, 4, 5]
		y = [10, 11, 12, 13, 14]
		fig = go.Figure()

		fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))
		fig.update_layout(title='Basic Line Chart', xaxis_title='X Axis', yaxis_title='Y Axis')

        # Convert plot to HTML
		plot_html = pio.to_html(fig, full_html=True)


		return HttpResponse(plot_html, content_type='text/html')