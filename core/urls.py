from django.urls import path
from django.contrib.auth.views import LoginView

#urlpatterns = [
    # outras URLs

#]
from .views import login, index, loadlogin

urlpatterns = [
    path('index/', index , name='index'),
    path('login/', login, name='login'),
    path('loadlogin/', loadlogin, name='loadlogin'),



    #path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]