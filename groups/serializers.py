from rest_framework import serializers

from groups.models import Group, GroupToUser
from users.serializers import UserProfileSerializer


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "group_name", "group_type", "group_description", "created_at", "deleted_at", "created_by_id", "is_active"]


class GroupToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupToUser
        fields = "__all__"




class GroupUserSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(required=False, many=True)
    class Meta:
        model = Group
        fields = ["group_name", "group_type", "group_description", "created_at", "deleted_at", "created_by_id", "is_active", "users"]