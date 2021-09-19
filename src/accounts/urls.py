from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_reset'),
	path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
]