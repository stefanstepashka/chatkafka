from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('chat/<int:pk>/', views.chat_view, name='chat_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('messages/', views.messages),
    path('', views.main_view, name='main_view'),
    path('signup/',views.signup_view, name='signup_view'),
    path('chat/create/', views.chat_create_view, name='chat_create_view'),
    path('messages/<int:chat_id>/', views.chat_messages, name='chat_messages'),
    path('chat/<int:chat_id>/manage_participant/', views.manage_participant_view, name='manage_participant'),

    path('api/chats/', views.chat_list, name='chat-list'),
    path('api/chats/<int:id>/', views.chat_detail, name='chat-detail'),
    path('api/messages/', views.MessageList.as_view()),
    path('api/messages/<int:pk>/', views.MessageDetail.as_view()),
    path('api/token/', obtain_auth_token, name='obtain-token'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
