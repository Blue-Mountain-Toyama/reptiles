from django.shortcuts import render

#############################################################################
# コーパスにデータを追加
#############################################################################
def index(request):
	params = {}

	if 'btn_send' in request.POST:
		text = request.POST['text']
		params['text'] = text

	return render(request, 'corpus/index.html', params)
