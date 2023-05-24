from rest_framework import serializers

from myblog.models import (
    Post,
    Comment,
)

class PostSerializer(serializers.ModelSerializer):
    class Meta():
        model = Post
        fields = ['id', 'author', 'title', 'text', 'picture', 'published_date']

class CommentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Comment 
        fields = ['id', 'post', 'author', 'text', 'create_date', 'approved_comment']

