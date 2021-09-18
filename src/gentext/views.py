<<<<<<< Updated upstream
from django.shortcuts import render
from django.http import HttpResponse
from transformers import T5Tokenizer, AutoModelForCausalLM

def index(request):
	tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
	tokenizer.do_lower_case = True
	model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt2-medium")

	input_text = "海へ行きたい"
	input_ids = tokenizer.encode(
		input_text,
		return_tensors="pt"
	)

	length = 40
	temperature = 1.0
	k = 0
	p = 0.9
	repetition_penalty = 1.0
	num_return_sequences = 3

	output_sequences = model.generate(
		input_ids=input_ids,
		max_length=length + len(input_text),
		temperature=temperature,
		top_k=k,
		top_p=p,
		repetition_penalty=repetition_penalty,
		do_sample=True,
		num_return_sequences=num_return_sequences,
	)

	generated_sequences = []

	for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
		generated_sequence = generated_sequence.tolist()

		text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

		total_sequence = (
			input_text + text[len(tokenizer.decode(input_ids[0], clean_up_tokenization_spaces=True)) :]
		)

		generated_sequences.append(total_sequence)


	return HttpResponse(generated_sequence)
=======
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from django.template import loader
from django.contrib import messages
from app.tasks import gentext
from urllib import parse

from logging import getLogger

#############################################################################
# 日記生成のトップ画面
#############################################################################
def index(request):
    return HttpResponse('hello')

#############################################################################
# 日記追加画面
#############################################################################
def add(request):
    # セッションの値をクリア
    request.session['task_id'] = ''
    return render(request, 'gentext/add.html')

#############################################################################
# 文章の生成と選択画面
#############################################################################
def select(request):
    params = {}

    # 送信ボタンが押されたら非同期で実行
    if 'btn_send' in request.POST and request.session['task_id'] == '':
        # 入力文章を取得
        input_text = request.POST['input_text']
        if len(input_text) < 1:
            return render(request, 'gentext/index.html', params)

        # 非同期実行
        task_id = gentext.delay(input_text)
        # task_idをセッションで保持
        request.session['task_id'] = str(task_id)

    # 結果を取得
    results = TaskResult.objects.all()

    # 結果が
    if len(results) == 0:
        results[0] == 0

    # セッションで保持したtask_idをもとに結果を取得
    if results[0].task_id == request.session['task_id']:
        params['result'] = parse.unquote(list(results.values_list('result', flat=True))[0].replace('\\\\', '\s\\'))
    else:
        params['result'] = 'wait'

    return render(request, 'gentext/select.html', params)
>>>>>>> Stashed changes
