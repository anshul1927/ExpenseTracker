from rest_framework import serializers

from groups.models import Group, GroupToUser


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupToUser
        fields = "__all__"
