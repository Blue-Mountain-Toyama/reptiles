from django.urls import path
from . import views

app_name = 'gentext'
urlpatterns = [
<<<<<<< Updated upstream
	path('', views.index, name="index"),
=======
	path('', views.index, name='index'),
	path('add/', views.add, name='add'),
	path('select/', views.select, name='select'),
>>>>>>> Stashed changes
]