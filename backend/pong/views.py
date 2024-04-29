from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	print ( type(request))
	print(request.GET.get("a"))
	return HttpResponse("Hello from pong game")
