from django.urls import path

from chatbot import views

app_name = "chatbot"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("chat/", views.chat, name="chat"),
    path("upload/", views.upload_knowledge, name="upload"),
]
