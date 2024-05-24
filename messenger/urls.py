from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('message/edit/<int:message_id>/',
         views.edit_message, name='edit_message'),
    path('message/delete/<int:message_id>/',
         views.delete_message, name='delete_message'),
]
