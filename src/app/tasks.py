from __future__ import absolute_import, unicode_literals
from celery import shared_task
from transformers import T5Tokenizer, AutoModelForCausalLM
import time
from django.core import serializers
from .scraper import scraper


#############################################################################
# rinnaモデルによる文章生成タスク
#############################################################################
@shared_task(bind=True)
def gentext(self, input_text):
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
        num_return_sequences = 10

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

        # 入力テキストをエンコード
        input_ids = tokenizer.encode(
            input_text,
            return_tensors='pt'
        )

        # 出力文章の生成
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

        # 生成文章の成形
        generated_sequences = []
        generated_sequences.append(illustration_file)

        for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
            generated_sequence = generated_sequence.tolist()

            # デコード
            text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

            total_sequence = (
                input_text + text[len(tokenizer.decode(input_ids[0], clean_up_tokenization_spaces=True)) :]
            )
            generated_sequences.append(total_sequence)

        return generated_sequences

    # リトライ用
    except Exception as exc:
        self.retry(exc=exc)
