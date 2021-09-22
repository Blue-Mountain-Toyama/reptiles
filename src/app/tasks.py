from __future__ import absolute_import, unicode_literals
from celery import shared_task
from transformers import T5Tokenizer, AutoModelForCausalLM
import time
from django.core import serializers
from .scraper import scraper
from .text_generator.word_creator import do_random, go_random, do_specific, go_specific, rand_generation


#############################################################################
# rinnaモデルによる文章生成タスク
#############################################################################
@shared_task(bind=True)
def gentext(self, input_text, type):
    try:
        illustration_file = scraper(input_text)

        #############################################################################
        # 設定
        #############################################################################
        length = 40
        temperature = 1.0
        k = 0
        p = 0.9
        repetition_penalty = 1.0
        num_return_sequences = 1

        # トークナイザ、モデルの読み込み
        try:
            tokenizer = T5Tokenizer.from_pretrained('./pretrained/tokenizer_rinna')
        except OSError:
            tokenizer = T5Tokenizer.from_pretrained('rinna/japanese-gpt2-medium')
            tokenizer.save_pretrained('/pretrained/tokenizer_rinna')
        tokenizer.do_lower_case = True
        try:
            model = AutoModelForCausalLM.from_pretrained('./pretrained/model_rinna', force_download=True)
        except OSError:
            model = AutoModelForCausalLM.from_pretrained('rinna/japanese-gpt2-medium')
            model.save_pretrained('/pretrained/model_rinna')


        # 出力の生成
        output_sequences = []
        generated_sequences = []
        generated_sequences.append(illustration_file)

        for i in range(5):
            # タイプに応じた文章の自動生成
            if type == 'place':
                created_text = go_specific(input_text)
            elif type == 'event':
                created_text = do_specific(input_text)
            print(created_text)

            # 入力テキストをエンコード
            input_id = tokenizer.encode(
                created_text,
                return_tensors='pt'
            )

            # 出力文章の生成
            output_sequence = model.generate(
                input_ids=input_id,
                max_length=length + len(created_text),
                temperature=temperature,
                top_k=k,
                top_p=p,
                repetition_penalty=repetition_penalty,
                do_sample=True,
                num_return_sequences=num_return_sequences,
            )


            # 生成文章の成形
            generated_sequence = output_sequence[0].tolist()

            # デコード
            text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

            total_sequence = (
                created_text + text[len(tokenizer.decode(input_id[0], clean_up_tokenization_spaces=True)) :]
            )
            print(total_sequence)
            generated_sequences.append(total_sequence)

        return generated_sequences

    # リトライ用
    except Exception as exc:
        self.retry(exc=exc)

#############################################################################
# rinnaモデルによる文章生成タスク
#############################################################################
@shared_task(bind=True)
def gentext_all(self, days):
    try:
        #############################################################################
        # 設定
        #############################################################################
        length = 40
        temperature = 1.0
        k = 0
        p = 0.9
        repetition_penalty = 1.0
        num_return_sequences = 1

        # トークナイザ、モデルの読み込み
        try:
            tokenizer = T5Tokenizer.from_pretrained('./pretrained/tokenizer_rinna')
        except OSError:
            tokenizer = T5Tokenizer.from_pretrained('rinna/japanese-gpt2-medium')
            tokenizer.save_pretrained('/pretrained/tokenizer_rinna')
        tokenizer.do_lower_case = True
        try:
            model = AutoModelForCausalLM.from_pretrained('./pretrained/model_rinna', force_download=True)
        except OSError:
            model = AutoModelForCausalLM.from_pretrained('rinna/japanese-gpt2-medium')
            model.save_pretrained('/pretrained/model_rinna')

        # 出力の生成
        output_sequences = []
        generated_sequences = []

        for i in range(days):
            content = rand_generation()
            created_text = content['text']
            keyword = content['keyword']

            # スクレイピング
            illustration_file = scraper(keyword)
            if illustration_file == '':
                illustration_file = 'none'
            generated_sequences.append(str(illustration_file))

            # 入力テキストをエンコード
            input_id = tokenizer.encode(
                created_text,
                return_tensors='pt'
            )

            # 出力文章の生成
            output_sequence = model.generate(
                input_ids=input_id,
                max_length=length + len(created_text),
                temperature=temperature,
                top_k=k,
                top_p=p,
                repetition_penalty=repetition_penalty,
                do_sample=True,
                num_return_sequences=num_return_sequences,
            )


            # 生成文章の成形
            generated_sequence = output_sequence[0].tolist()

            # デコード
            text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

            total_sequence = (
                created_text + text[len(tokenizer.decode(input_id[0], clean_up_tokenization_spaces=True)) :]
            )
            if total_sequence == '':
                total_sequence = created_text
            print(total_sequence)
            generated_sequences.append(str(total_sequence))

        return generated_sequences

    # リトライ用
    except Exception as exc:
        self.retry(exc=exc)


