from django.urls import path, include
from .views import login, index, loadlogin, logouts, cadastro

#urlpatterns = [
   # path('index/', index , name='index'),
   # path('', login, name='login'),
  #  path('loadlogin/', loadlogin, name='loadlogin'),
 #   path('logouts/', logouts, name='logouts'),

#]
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('loadlogin/', loadlogin, name='loadlogin'),
    path('logouts/', logouts, name='logouts'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cadastro/', cadastro, name='cadastro'),
]
