from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'username', 'content', 'timestamp', 'chat']


class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    admin = UserSerializer()
    messages = MessageSerializer(source='message_set', many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'participants', 'admin', 'messages']