from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.request import QueryDict


from django.contrib.auth.models import User

from posts.filters import PostslFilter
from posts.models import Posts, Comments

from posts.serializers import (
    PostsSerializer,
    PostsCreateSerializer,
    PostsCreateSaveSerializer,
    CommentsSerializer,
    CommentsSaveSerializer,
)


class PostsAPICreate(generics.CreateAPIView):
    """Контроллер для создании постов"""
    queryset = Posts.objects.all()
    serializer_class = PostsCreateSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        querydict = QueryDict(mutable=True)
        querydict['csrfmiddlewaretoken'] = request.data['csrfmiddlewaretoken']
        querydict['title'] = request.data['title']
        querydict['text'] = request.data['text']
        querydict['user'] = str(request.user.id)
        post_serializer = PostsCreateSaveSerializer(data=querydict)
        post_serializer.is_valid()
        post_serializer.save()
        return Response(status=201)


def get_comments(comments) -> list[dict]:
    list_comments = []
    for comment in comments:
        dict_comment = {}
        dict_comment['username'] = User.objects.get(id=CommentsSaveSerializer(comment).data['user']).username
        dict_comment['text'] = CommentsSaveSerializer(comment).data['text']
        list_comments.append(dict_comment)

    return list_comments

class PostsAPI(generics.RetrieveUpdateDestroyAPIView):
    """Контроллер для получения, изменения и удалении постов"""
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = PostslFilter
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        try:
            post = Posts.objects.get(id=kwargs['pk'])
        except Posts.DoesNotExist:
            return Response({'response': f'Данных под индексом {kwargs['pk']} нету'})

        dict_post = PostsSerializer(post).data
        dict_post['user'] = User.objects.get(id=dict_post['user']).username

        try:
            comments = Comments.objects.filter(post_id=kwargs['pk'])
        except Comments.DoesNotExist:
            response = {
                'post': dict_post,
            }
            return Response(response)

        list_comments = get_comments(comments)

        response = {
            'post': dict_post,
            'comments': list_comments
        }
        return Response(response)

class CommentsAPICreate(generics.CreateAPIView):
    """Контроллер для создании коментариев"""
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticated, )


    def post(self, request, *args, **kwargs):
        querydict = QueryDict(mutable=True)
        querydict['csrfmiddlewaretoken'] = request.data['csrfmiddlewaretoken']
        querydict['text'] = request.data['text']
        querydict['post'] = request.data['post']
        querydict['user'] = str(request.user.id)
        post_serializer = CommentsSaveSerializer(data=querydict)
        post_serializer.is_valid()
        post_serializer.save()
        return Response(status=201)

class PostListAPI(generics.ListAPIView):
    """Контролер для вывода всех постов и их фильтрации по заголовку и дате"""
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PostslFilter