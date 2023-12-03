from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video/<str:video_user>/<int:index>', views.video, name='video'),
    path('upload-video', views.upload, name='upload'),
    path('like-video', views.like, name='like'),
]
