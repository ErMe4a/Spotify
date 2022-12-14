from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics,permissions, response
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.permissons import IsAccountOwner, IsAuthor
from account import views
from .models import Favorites
from .serializers import FavoritesSerializer
from music.models import Music
from . import serializers
from .models import Comment



User = get_user_model()

class CommentListCreateView(generics.ListCreateAPIView):
    
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthor,)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

class FavoritesView(views.APIView):
    permission_classes = (IsAccountOwner,)

    def get(self,request):
        user = request.user
        favorites =  user.favorites.all()
        serializer = FavoritesSerializer(favorites, many = True)
        return Response(serializer.data)


