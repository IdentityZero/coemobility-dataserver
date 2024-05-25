from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.createNewConversation),
    path("conversations/", views.ConversationListView.as_view()),
    path("conversations/messages/<int:conversation>/", views.MessageListView.as_view()),
    path("conversations/messages/create/", views.MessageCreateView.as_view()),
]