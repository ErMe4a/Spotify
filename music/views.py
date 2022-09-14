from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
import account

from spotify.tasks import send_beat_email
from .models import Music
from . import serializers
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from comments_and_likes.serializers import CommentSerializer,LikeSerializer, FavoritesSerializer
from comments_and_likes.models import Like,Favorites
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from account.permissons import IsAccountOwner
from account.send_email import send_notification
from .serializers import MusicCreateSerializer


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000


class MusicViewSet(ModelViewSet):
    queryset = Music.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('name',)
    pagination_class = StandartResultPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MusicListSerializer
        return serializers.MusicDetailSerializer

    def get_permissions(self):
        # Создавать может залогиненный юзер
        if self.action in ( 'create','add_to_liked', 'remove_from_liked','get_likes', ):
            return [permissions.IsAuthenticated()]
        # Изменять и удалять может только исполнитель
        elif self.action in ('update', 'partial_update', 'destroy', ):
            return [permissions.IsAdminUser(), IsAccountOwner()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny()]

    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        music = self.get_object()
        if request.method =='GET':
            reviews =  music.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status = 200)
        data = request.data 
        serializer = ReviewSerializer(data = data, context={'request':request, 'music':music})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=201)

    
    @action(['GET'], detail=True, )
    def comments(self, request, pk):
        music = self.get_object()
        comments = music.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return response.Response(serializer.data, status=200)

    @action(['POST'], detail=True, )
    def add_to_liked(self, request, pk):
        music = self.get_object()
        if request.user.liked.filter(music=music).exists():
            return response.Response('Вы уже поставили свой лайк!', status=400)
        Like.objects.create(music=music, owner=request.user)
        return response.Response('Вы поставили лайк', status=201)

    
    @action(['POST'], detail=True, )
    def remove_from_liked(self, request, pk):
        music = self.get_object()
        if not request.user.liked.filter(music=music).exists():
            return response.Response('Вы не лайкали этот пост', status=400)
        request.user.liked.filter(music=music).delete()
        return response.Response('Ваш лайк удален!', status=204)

    @action(['GET'], detail=True, )
    def get_likes(self, request):
        music = self.get_object()
        likes = music.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return response.Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        music= self.get_object()
        if request.user.favorites.filter(music=music).exists():
            request.user.favorites.filter(music=music).delete()
            return response.Response('Убрали из избранных', status=204)
        Favorites.objects.create(music=music, owner=request.user)
        return response.Response('Добавлено в избранные!', status=201)

    # @action(['GET'], detail=True)
    # def top(self,request):
    #     music = Music.objects.all()
    #     tops = music.reviews.all()
    #     serializer = serializers.TopSerializer(tops, many = True)
    #     return response.Response(serializer, status=200)







        


    

