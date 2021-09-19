from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#############################################################################
# コーパスにデータを追加
#############################################################################
@login_required
def index(request):
	params = {}

	if 'btn_send' in request.POST:
		text = request.POST['text']
		params['text'] = text

	return render(request, 'corpus/index.html', params)
