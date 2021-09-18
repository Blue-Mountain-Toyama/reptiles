from django.shortcuts import render

#############################################################################
# ファインチューニング用のテキスト投入
#############################################################################
def index(request):
	params = {}
	return render(request, 'data/index.html', params)
