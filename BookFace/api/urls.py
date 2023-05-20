from django.urls import path

from . import views 

urlpatterns = [
    path('postlist/',
         views.PostList.as_view()),
    path('commentlist/',
         views.CommentList.as_view())
]