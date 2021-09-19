from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def signup(request):
	params = {
		'form': None,
	}

	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		# バリデーション
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.info(request, '登録が完了しました。')
			return redirect('index')
	else:
		form = UserCreationForm()

	params['form'] = form

	return render(request, 'accounts/signup.html', params)