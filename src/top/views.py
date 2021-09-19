from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
	params = {}
	return render(request, 'top/index.html', params)