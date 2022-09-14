from dataclasses import field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from comments_and_likes.serializers import FavoritesSerializer
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy
from .models import Contact

User = get_user_model()


class RegistrerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=100, required=True, write_only=True)
    password_repeat  = serializers.CharField(min_length=6, max_length=100, required=True, write_only=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'password_repeat')

    def validate(self, attrs):
        password_repeat  = attrs.pop('password_repeat')
        if attrs.get('password') != password_repeat :
            raise serializers.ValidationError('Password did not match!')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Password field must be contain alpha symbols and numbers !')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(email = email, password = password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        else: 
            raise serializers.ValidationError('Invalid password!')
        return attrs



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': ('Token is invalid or expired!')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)


class RestorePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=6, required=True)
    password_repeat = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        password_repeat  = attrs.pop('password_repeat')
        if password_repeat  != attrs['password']:
            raise serializers.ValidationError('Пароли не совпадают')

        try:
            user = User.objects.get(activation_code=attrs['code'])
        except User.DoesNotExist:
            serializers.ValidationError('Ваш код неверен!')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.set_password(data['password'])
        user.activation_code = ''
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['favorites'] = FavoritesSerializer(instance.favorites.all(),many=True).data
        return repr

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'date_joined')
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['favorites'] = FavoritesSerializer(instance.favorites.all(),many=True).data
        return repr

class SpamViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'