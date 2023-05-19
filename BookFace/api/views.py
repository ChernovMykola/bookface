from django.shortcuts import render
from .serializers import (
    PostSerializer,
    CommentSerializer
)
from rest_framework import (
    generics,
    permissions,
)
from myblog.models import (
    Post,
    Comment
)

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Post.objects
    
class CommentList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Comment.objects