from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Post, Comment, Trend, PostAttachment


class PostAttchmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttchmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'is_private', 'comments_count', 'likes_count', 'created_by', 'created_at_formatted', 'attachments',)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = PostAttchmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'comments', 'comments_count', 'attachments')

class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)

