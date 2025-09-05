from django.urls import path, include
from .views import (
    landing, index, register_view, response, login_view,
    fetch_chats, get_conversations
)

urlpatterns = [
    path('', landing, name='landing'),
    path('chat', index, name='index'),
    path('accounts/register/', register_view, name='register'),
    path('response', response, name='response'),
    path('login', login_view, name='login'),
    path('fetch-chats', fetch_chats, name='fetch_chats'),
    path('get-conversations', get_conversations, name='get_conversations'),
]

