from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id','topic', 'latest_message']
    
    def get_latest_message(self,obj):

        latest = Message.objects.filter(conversation=obj).order_by('-id').first()
        if latest:
            return latest.body[:50]
        return None


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        