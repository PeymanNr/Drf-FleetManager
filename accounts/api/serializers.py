from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already in use.')
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('The password must be at least 6 characters long.')
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError('Password must contain at least one number.')
        if not any(char.islower() for char in value):
            raise serializers.ValidationError('The password must contain at least one lowercase letter.')
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError('Password must contain at least one capital letter.')
        return value

    def create(self, validated_data):
        password = validated_data.get('password')
        hashed_password = make_password(password)
        user = User.objects.create(
            username=validated_data['username'],
            password=hashed_password,
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['registration_step'] = user.registration_step

        return token


