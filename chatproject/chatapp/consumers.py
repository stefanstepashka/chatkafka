import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaProducer
from .models import Message, Chat
from kafka import KafkaConsumer
from channels.db import database_sync_to_async




class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.producer = KafkaProducer(bootstrap_servers='kafka:9092')


    async def disconnect(self, close_code):
        # Cancel the loop that is running in the background
        self.read_messages_task.cancel()
        # Close the producer
        self.producer.close()
        # Close the consumer
        self.consumer.close()

    @database_sync_to_async
    def create_message(self, username, message, chat_id):
        chat = Chat.objects.get(id=chat_id)
        Message.objects.create(username=username, content=message, chat=chat)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_id = text_data_json['chat_id']
        await self.create_message(self.scope['user'].username, message, chat_id)

        # send message to Kafka
        self.producer.send('chat_messages', value=message.encode('utf-8'))

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        await self.accept()

        # create Kafka consumer
        self.consumer = KafkaConsumer(
            'chat_messages',
            bootstrap_servers='kafka:9092',
            consumer_timeout_ms=1000)

        # start reading messages from Kafka in the background
        self.read_messages_task = asyncio.ensure_future(self.read_messages())

    async def read_messages(self):
        try:
            for message in self.consumer:
                # decode the message and send it to all connected clients
                await self.send(text_data=json.dumps({
                    'message': message.value.decode('utf-8')
                }))
        except Exception as e:
            print("Error in read_messages: ", e)
            raise e