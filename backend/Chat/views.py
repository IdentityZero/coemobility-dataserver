from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from rest_framework import generics

from .models import Conversation, Message
from .serializers import ConversationSerializer,MessageSerializer

@csrf_exempt
def createNewConversation(request):
    if not request.method == "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # Get data
    data = json.loads(request.body)
    user_id = int(data['user'])
    user = User.objects.get(pk=user_id)
    topic = data['topic']
    body = data['newtopicbody']
    
    # Create new objects
    newConvo = Conversation.objects.create(creator=user, topic=topic)

    Message.objects.create(sender=user,conversation=newConvo, body=body)
    
    return JsonResponse({'message': 'New conversation created'}, status=201)

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                if user.is_superuser:
                    return Conversation.objects.all().order_by('-id');
                return Conversation.objects.filter(creator=user).order_by('-id')
            except:
                pass

        return Conversation.objects.none()

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation = Conversation.objects.get(pk=self.kwargs['conversation'])
        qs = Message.objects.filter(conversation=conversation).order_by('-id')
        return qs


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

