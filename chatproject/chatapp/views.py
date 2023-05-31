from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Message
from .forms import ChatForm, ParticipantForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Chat
from django.contrib.auth.forms import UserCreationForm

from rest_framework import generics, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Chat

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main_view')
    else:
        form = UserCreationForm()
    return render(request, 'chatapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_view')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'chatapp/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'chatapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


def chat_view(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    participants = chat.participants.all()
    return render(request, 'chatapp/chat.html', context={'chat_id': pk, 'participants': participants,
                                                         'user': request.user, 'chat':chat
                                                         })


def messages(request):
    messages = Message.objects.order_by('-timestamp').all()[:50]
    messages = list(messages.values('username', 'content', 'timestamp'))
    return JsonResponse(messages, safe=False)


def chat_messages(request, chat_id):
    messages = Message.objects.filter(chat_id=chat_id).order_by('-timestamp').all()[:50]
    messages = list(messages.values('username', 'content', 'timestamp'))
    return JsonResponse(messages, safe=False)


def chat_create_view(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.admin = request.user
            chat.save()
            for user in form.cleaned_data['participants']:
                chat.participants.add(user)
                chat.save()

            return redirect('main_view')
    else:
        form = ChatForm()
    return render(request, 'chatapp/chat_create.html', {'form': form})

def main_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    chats = Chat.objects.filter(participants=request.user)

    context = {'user': request.user, 'chats': chats}
    return render(request, 'chatapp/main.html', context)


def manage_participant_view(request, chat_id):
    if request.method == 'POST':
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=request.POST['user_id'])
        action = request.POST['action']
        if chat.admin == request.user:
            if action == 'add':
                chat.participants.add(user)
            elif action == 'remove' and request.user != user:
                chat.participants.remove(user)
            chat.save()
        return redirect('chat_view', pk=chat_id)





#API

class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]





@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.filter(users=request.user)
        return Response({'chats': chats})

    elif request.method == 'POST':
        chat = Chat.objects.create()
        chat.users.add(request.user)
        return Response({'detail': 'Chat created'})


@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_detail(request, id):
    chat = Chat.objects.get(id=id)
    if request.user not in chat.users.all():
        return Response({'detail': 'Not authorized'}, status=403)

    if request.method == 'GET':
        return Response({'chat': chat})

    elif request.method == 'DELETE':
        chat.delete()
        return Response({'detail': 'Chat deleted'})