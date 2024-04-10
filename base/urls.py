from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('post-details/<str:pk>', views.postdetails, name="postdetails"),
    path('create-post/', views.createPost, name="createpost"),
    path('update-post/<str:pk>', views.updatePost, name="updatepost"),
    path('delete-post/<str:pk>', views.deletePost, name="deletepost")
]
