from django.urls import path

from . import views 

urlpatterns = [
    path('postlist/',
         views.PostList.as_view()),
    path('commentlist/',
         views.CommentList.as_view()),
    path('signup/',
        views.signup),
    path('login/',
        views.login),
    path('postlist/<int:pk>',
        views.PostRetrieveUpdateDestroy.as_view()),
]