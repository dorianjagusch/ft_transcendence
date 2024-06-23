from django.urls import path
from .views import StatsView

urlpatterns = [
    path('stats/', StatsView.as_view(), name='stats_view'),
]
