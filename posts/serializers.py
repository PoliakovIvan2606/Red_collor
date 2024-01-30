from rest_framework import serializers
from .models import Posts, Comments
from django.contrib.auth.models import User

# получение поста
class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'title', 'text', 'user']

# Создание поста
class PostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['title', 'text']

class PostsCreateSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"



# Создание коментария
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text', 'post']

class CommentsSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"


# Для получения коментариев при получении поста
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentsPostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comments
        fields = ['user', 'text']
