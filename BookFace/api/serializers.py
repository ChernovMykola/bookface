from rest_framework import serializers

from myblog.models import (
    Post,
    Comment,
)

class PostSerializer(serializers.modelSerializer):
    class Meta():
        model = Post
        fields = ['id', 'author', 'title', 'text', 'picture', 'create_day', 'published_date']

class CommentSerializer(serializers.modelSerializer):
    class Meta():
        model = Comment 
        fields = ['id', 'post', 'author', 'text', 'create_date', 'approved_comment']
