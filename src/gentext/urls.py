from django.urls import path
from . import views

app_name = 'gentext'
urlpatterns = [
	path('', views.index, name='index'),
	path('generate/', views.generate, name='generate'),
	path('select/', views.select, name='select'),
]