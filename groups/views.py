from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Group, GroupToUser
from .serializers import GroupSerializer, GroupToUserSerializer


# Create your views here.

class GroupsList(APIView):
    def get(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GroupDetails(APIView):
    def get(self, request, id):
        group = get_object_or_404(Group, pk=id)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, id):
        group = get_object_or_404(Group, pk=id)
        serializer = GroupSerializer(group, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        group = get_object_or_404(Group, pk=id)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupUsersList(APIView):
    def get(self, request, id):
        queryset = GroupToUser.objects.filter(group_id=id)
        serializer = GroupToUserSerializer(queryset, many=True)
        return Response(serializer.data)


class AddUserToGroup(APIView):
    def post(self, request):
        serializer = GroupToUserSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
