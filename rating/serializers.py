from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user =serializers.ReadOnlyField(source = 'user.email')
    music = serializers.ReadOnlyField(source = 'music.name')
    class Meta:
        model = Review
        fields = '__all__'

    def create(self , validated_data):
        request =self.context.get('request')
        user = request.user 
        music = self.context.get('music')
        validated_data['user'] = user
        validated_data['music'] = music
        return super().create(validated_data)

