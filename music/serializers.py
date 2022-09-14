from pyexpat import model
from rest_framework import serializers
from .models import Music
from django.db.models import Avg
from comments_and_likes.serializers import CommentSerializer


class MusicListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta :
        model = Music
        fields = ('id','name','category','song','image','creator','comments')

    def is_liked(self,music):
        user = self.context.get('request').user
        return user.liked.filter(music=music).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr

class MusicDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta: 
        model = Music
        fields = '__all__'
    def is_liked(self,music):
        user = self.context.get('request').user
        return user.liked.filter(music=music).exists()
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews'] = instance.reviews.count()
        return repr

class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

# class TopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Music
#         fields = ('name', 'rating')

#     def to_representation(self, instance):
#         repr = super().to_representation(instance)
#         repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        
#         return repr