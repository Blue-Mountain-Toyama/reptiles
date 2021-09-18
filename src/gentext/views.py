from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from django.template import loader
from django.contrib import messages
from app.tasks import gentext
from urllib import parse
import re
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
        # 表示文字列の成形
        molded_results = list(results.values_list('result', flat=True))[0]
        # 不要な文字をトリム
        molded_results = re.sub(r'\[|\]|\"', '', molded_results)
        # 文字列のデコード
        molded_results = molded_results.encode().decode('unicode-escape')
        # 文字列をカンマで分割してリスト化
        molded_results = molded_results.split(',')
        params['results'] = molded_results
    else:
        params['results'] = 'wait'

    return render(request, 'gentext/select.html', params)
