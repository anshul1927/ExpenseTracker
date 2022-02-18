from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users import serializers, models
from django.http import HttpResponse
import json
from datetime import date, datetime
from decimal import Decimal
from rest_framework.renderers import JSONRenderer


# Create your views here.
class CreateUserAPIView(APIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request) -> Response:
        """Create a Hello msg with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            name = serializer.validated_data.get('first_name')
            return Response({'message': f'user {name} created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JsonENcoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return super().default(obj)


class getUserList(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            print("1")
            _user_data = models.User.objects.values_list('first_name', 'last_name', 'email')
            print("2")
            _user_list = list(_user_data)
            print("3")
            # return Response(json.dumps({'data': _user_list}, cls=JsonENcoder), status=200)
            content = {'_user_data': _user_data}
            content1 = {'_user_list':_user_list}
            return Response(content1)
        except Exception as e:
            error_msg = "Internal Error Occurred"
            return Response(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }, cls=JsonENcoder), status=500)
