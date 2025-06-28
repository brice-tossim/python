from django.urls import path

from api.views.chat.index import ChatView


urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
]
