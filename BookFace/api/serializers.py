from rest_framework import serializers

from myblog.models import (
    Post,
    Comment,
)

class PostSerializer(serializers.modelSerializer):
    class Meta():
        model = Post
        fields = ['id', 'author', 'title', 'text', 'picture', 'create_day', 'published_date']

