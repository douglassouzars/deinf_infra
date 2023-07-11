from django.urls import path, include
from .views import logouts , cadastro, loadcadastro, index, loadlogin, mapeamento, get_users_from_group, get_all_users, add_user_to_group, adicionar_usuario, remover_usuario, atualizar_mapeamento, get_subchefe
#from .views import LoadloginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import  TemplateView
from django.contrib.auth import login , logout
from core import views


urlpatterns = [
    path('index/', index, name='index'),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('loadlogin/', loadlogin, name='loadlogin'),
    path('logouts/', logouts, name='logouts'),
    path('adicionar_usuario/', adicionar_usuario, name='adicionar_usuario'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cadastro/', cadastro, name='cadastro'),
    path('loadcadastro/',loadcadastro, name='loadcadastro'),
    path('mapeamento/', mapeamento, name='mapeamento'),
    path('get_users_from_group/', views.get_users_from_group, name='get_users_from_group'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('add_user_to_group/', views.add_user_to_group, name='add_user_to_group'),
    path('remover_usuario/', views.remover_usuario, name='remover_usuario'),
    path('atualizar_mapeamento/', views.atualizar_mapeamento, name='atualizar_mapeamento'),
    path('get_subchefe/', get_subchefe, name='get_subchefe'),
]
