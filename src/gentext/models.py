from django.db import models
from django.conf import settings

#############################################################################
# 日記
#############################################################################
class Diary(models.Model):
	user		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name		= models.CharField(max_length=16, verbose_name='日記名', default='My Diary')
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = '日記'

#############################################################################
# 日記の各ページ用
#############################################################################
class DiaryPage(models.Model):
	diary		= models.ForeignKey(Diary, on_delete=models.CASCADE)
	date		= models.DateTimeField(verbose_name='日付')
	keyword		= models.CharField(max_length=62, verbose_name='キーワード')
	body		= models.TextField(verbose_name='本文')
	img_path	= models.CharField(max_length=256, verbose_name='画像パス', default='')
	is_public	= models.BooleanField(verbose_name='公開フラグ', default=False)
	created_at	= models.DateTimeField(auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.body

	class Meta:
		verbose_name_plural = '日記ページ'
