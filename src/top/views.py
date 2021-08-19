from django.shortcuts import render

def index(request):
	params = {
		"msg": "Hello, world",
	}
	return render(request, 'top/index.html', params)