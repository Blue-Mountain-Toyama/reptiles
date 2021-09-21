from django.urls import path
from . import views

app_name = 'gentext'
urlpatterns = [
	path('', views.index, name='index'),
	path('generate/', views.generate, name='generate'),
	path('generate_all/', views.generate_all, name='generate_all'),
	path('select/', views.select, name='select'),
	path('result_all/', views.result_all, name='result_all'),
]