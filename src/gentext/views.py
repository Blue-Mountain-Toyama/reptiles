from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.tasks import gentext, scraper
from urllib import parse
import re, os
from logging import getLogger
from .models import Diary, DiaryPage

#############################################################################
# 日記生成のトップ画面
#############################################################################
@login_required
def index(request):
    params = {}

    # 日記を取得、あるいは新規作成
    diary, create = Diary.objects.get_or_create(user=request.user)
    diary_pages = DiaryPage.objects.filter(diary=diary.id)
    params['pages'] = diary_pages

    # セッションの値をクリア
    request.session['task_id'] = ''
    request.session['input_text'] = ''

    return render(request, 'gentext/index.html', params)

#############################################################################
# 日記追加画面
#############################################################################
@login_required
def generate(request):
    params = {}

    # セッションの値をクリア
    request.session['task_id'] = ''
    request.session['input_text'] = ''
    return render(request, 'gentext/generate.html', params)

#############################################################################
# 文章の生成と選択画面
#############################################################################
@login_required
def select(request):
    params = {}

    # 送信ボタンが押されたら非同期で実行
    if 'btn_send' in request.POST and request.session['task_id'] == '':

        date = request.POST['diary_date']
        if len(date) < 1:
            messages.error(request, "日記の日付を指定してください。")
            return redirect('gentext:generate')

        # 入力文章を取得
        input_text = request.POST['input_text']
        if len(input_text) < 1:
            messages.error(request, "キーワードを入力してください。")
            return redirect('gentext:generate')

        # 非同期実行
        task_id = gentext.delay(input_text)
        # 値をセッションで保持
        request.session['input_text'] = input_text
        request.session['date'] = date
        request.session['task_id'] = str(task_id)

    # 結果を取得
    results = TaskResult.objects.all()

    # 結果が取得できるまでは待機
    if len(results) == 0:
        results[0] == 0

    # セッションで保持したtask_idをもとに結果を取得
    if results[0].task_id == request.session['task_id']:
        # 表示文字列の成形
        molded_results = list(results.values_list('result', flat=True))[0]
        # 不要な文字をトリム
        molded_results = re.sub(r'\[|\]|\"', '', molded_results)
        # 文字列をカンマで分割してリスト化
        molded_results = molded_results.split(',', 1)

        # 結果を分割取得
        illustration_file = '/static/img/illustration/' + molded_results[0]
        texts = molded_results[1]
        # 文字列のデコード
        texts = texts.encode().decode('unicode-escape')
        # 文字列をカンマで分割してリスト化
        texts = texts.split(',')

        params['results'] = texts
        params['illustration_file'] = illustration_file
    else:
        params['results'] = 'wait'


    # 決定ボタンが押されたら
    if 'btn_decide' in request.POST:
        diary = Diary.objects.get(user=request.user)

        diary_page = DiaryPage()
        diary_page.diary = diary
        diary_page.date = request.session['date']
        diary_page.keyword = request.session['input_text']
        diary_page.body = request.POST['text']
        diary_page.img_path = request.POST['image']
        diary_page.save()

        # セッションクリア
        request.session['task_id'] = ''
        request.session['input_text'] = ''
        request.session['date'] = ''

        messages.info(request, '日記を作成しました。')
        return redirect('gentext:index')

    return render(request, 'gentext/select.html', params)
