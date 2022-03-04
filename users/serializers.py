from rest_framework import serializers
from users import models




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = models.User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class signInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'password')