from django.urls import path
from .views import user_login, signup, chat_home, chat_interface,index

urlpatterns = [
     path('', index, name='index'), 
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('chat/', chat_home, name='chat_home'),
    path('chat/<str:username>/', chat_interface, name='chat_interface'),
]