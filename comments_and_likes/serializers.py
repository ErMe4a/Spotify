from rest_framework import serializers
from .models import Comment,Like,Favorites
from music.models import Music


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = ('id','body','owner','music')


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Like
        fields =('owner',)
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id','name','song','image',)
class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('music',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['music'] = MusicSerializer(instance.music).data
        return repr
