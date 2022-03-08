import imp
from multiprocessing.spawn import import_main_path
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from expenses.models import Debts
from expenses.serializers import DebtsSerializer
from expenses.views import update_user_balance
from .models import Group, GroupToUser
from .serializers import GroupSerializer, GroupToUserSerializer, GroupUserSerializer
from datetime import datetime
import json
import jwt
from .models import User
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes


def _same_groupname_user_exists(createdby, _group_name):
    try:
        group_name_list = list(
            GroupToUser.objects.filter(user_id=createdby).values_list(flat=False))

        print(group_name_list)
        if _group_name in group_name_list:
            return True
        return False
    except Exception as e:
        print(e)
        return True


# @csrf_exempt
# @login_required
class create_group(APIView):

    def post(self, request) -> Response:
        try:

            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            try:
                print(token)
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                print(payload)
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

            # user = User.objects.filter(id=payload['id']).first()
            _user_id = payload['id']
            _group_name = request.POST.get('group_name')

            _group_type = request.POST.get('type')
            _description = request.POST.get('description')
            _user_ids_list = json.loads(request.POST.get('users'))
            createdby = User.objects.filter(id=_user_id).first()

            if not _same_groupname_user_exists(createdby, _group_name):
                _group_obj = Group(group_name=_group_name, group_type=_group_type, group_description=_description,
                                   created_at=datetime.utcnow(), created_by=createdby, is_active=1)

                _group_obj.save()
                _user_ids_list.append(_user_id)
                list_user_obj = User.objects.filter(id__in=_user_ids_list)
                for user_obj in list_user_obj:
                    GroupToUser.objects.create(group_id=_group_obj, user_id=user_obj, is_active=1)
                return Response(json.dumps({
                    'message': 'Group Created Successfully',
                    'status': 'success'
                }), status=200)
            else:
                return Response(json.dumps({
                    'message': 'Same Name Group already exists for user',
                    'status': 'fail'
                }), status=400)
        except Exception as e:
            print(e)
            error_msg = "Internal Error Occurred"
            return Response(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }), status=500)


class get_group_data_for_user(ListAPIView):
    serializer_class = GroupSerializer

    def get(self, request) -> Response:
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            try:
                print(token)
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                print(payload)
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')

            _user_id = payload['id']
            _user = User.objects.filter(id=_user_id).first()

            if not _user:
                return Response(json.dumps({
                    'message': 'User Invalid / Inactive',
                    'status': 'Fail'
                }), status=400)

            _group_obj_list = GroupToUser.objects.filter(user_id=_user).values_list('group_id', flat=True)
            _list_group_id = list(_group_obj_list)

            _group_data = Group.objects.filter(id__in=_list_group_id).values()

            serializer = GroupSerializer(_group_data, many=True)
            # print(serializer.data)

            # queryset = _group_data.first()
            # print(queryset)
            # print(type(_group_data))
            # return Response(json.dumps({
            #     'data': serializer.data,
            #     'status': 'Success'
            # }, default=str), status=200)
            return Response(_group_data)
        except Exception as e:
            print(e)
            error_msg = "Internal Error Occurred"
            return Response(json.dumps({
                'message': error_msg,
                'status': 'Fail'
            }), status=500)


class get_group_detail(APIView):
    serializer_class = GroupSerializer

    def post(self, request):
        try:
            _group_id = request.POST.get('group_id')
            _group_obj = Group.objects.filter(id=_group_id, is_active=1).values()
            print(_group_obj.exists())
            if not _group_obj.exists():
                return Response(json.dumps({
                    'message': 'Group not exist',
                    'status': 'fail'
                }), status=400)

            _group_details = list(_group_obj)[0]
            if None in [_group_obj]:
                return Response(json.dumps({
                    'message': 'User Invalid / Inactive',
                    'status': 'fail'
                }), status=400)

            _group_users = GroupToUser.objects.filter(group_id=_group_obj.first()['id']).values_list('user_id_id',
                                                                                                     flat=True)
            _list_users = list(_group_users)
            _list_user_objs = list(User.objects.filter(id__in=_list_users).values())
            _group_details['users'] = _list_user_objs
            # serializer = GroupUserSerializer(_group_details, many=True)
            # print(_group_details)
            # print(serializer.data)

            return Response(_group_details)
            # return Response(json.dumps({
            #     'data': _group_details,
            #     'status': 'success'
            # }, default=str), status=200)
        except Exception as e:
            error_msg = "Internal Error Occurred"
            print(e)
            return Response(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }), status=500)


class delete_group(APIView):
    def post(self, request):
        try:
            _group_id = request.POST.get('group_id')
            print(_group_id)
            __group_obj = Group.objects.filter(id=_group_id, is_active=1)
            print(__group_obj)

            if None in __group_obj:
                return Response(json.dumps({
                    'message': 'Invalid Request',
                    'status': 'fail'
                }), status=400)

            print(__group_obj)
            __group_obj.update(**{
                'is_active': 0,
                'deleted_at': datetime.utcnow()
            })

            print(__group_obj)
            return Response(json.dumps({
                'message': 'Group Deleted Successfully',
                'status': 'success'
            }), status=200)
        except Exception as e:
            error_msg = "Internal Error Occurred"
            return HttpResponse(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }), status=500)




class remove_member_from_group(APIView):

    def post(self, request) -> Response:
        try:

            _group_id = request.POST.get('group_id')
            _remove_userid = request.POST.get('member_id')

            print(_group_id)
            print(_remove_userid)
            _group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
            _member_obj = User.objects.filter(id=_remove_userid).first()
            print(_group_obj)
            print(_member_obj)
            if None in [_group_obj, _member_obj]:
                return Response(json.dumps({
                    'message': 'Invalid Request',
                    'status': 'fail'
                }), status=400)
            GroupToUser.objects.filter(group_id=_group_obj, user_id=_member_obj).update(is_active=0)

            return Response(json.dumps({
                'message': 'Member Removed Successfully',
                'status': 'success'
            }), status=200)
        except Exception as e:
            print(e)
            error_msg = "Internal Error Occurred"
            return Response(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }), status=500)



class add_new_member(APIView):
    def post(self, request) -> Response:
        try:

            _group_id = request.POST.get('group_id')
            _member_id = request.POST.get('member_id')

            _group_obj = Group.objects.filter(id=_group_id, is_active=1).first()
            _member_obj = User.objects.filter(id=_member_id).first()

            if None in [_group_obj, _member_obj]:
                return Response(json.dumps({
                    'message': 'Invalid Request',
                    'status': 'fail'
                }), status=400)

            if GroupToUser.objects.filter(user_id=_member_obj, group_id=_group_obj, is_active=1).exists():
                return Response(json.dumps({
                    'message': 'Member already exists',
                    'status': 'success'
                }), status=400)
            elif GroupToUser.objects.filter(user_id=_member_obj, group_id=_group_obj, is_active=0).exists():
                GroupToUser.objects.filter(user_id=_member_obj, group_id=_group_obj).update(is_active=1)
            else:
                GroupToUser.objects.create(user_id=_member_obj, group_id=_group_obj)
            return Response(json.dumps({
                'message': 'Member Added Successfully',
                'status': 'success'
            }), status=200)
        except Exception as e:
            error_msg = "Internal Error Occurred"
            return Response(json.dumps({
                'message': error_msg,
                'status': 'fail'
            }), status=500)




class UserGroupDebts(APIView):
    def get(self, request, id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            print(token)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        # result = Expense.objects.prefetch_related('expense_user').all()
        queryset = Debts.objects.filter(group_id=id, payer=user_id)
        serializer = DebtsSerializer(queryset, many=True)

        return Response(serializer.data)


class Pay(APIView):
    def post(self, request, id):

        expense_id = request.POST.get('expense_id')
        receive = request.POST.get('bearer')
        pay_amt = request.POST.get('amount')
        print(request)

        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            print(token)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        print(1)
        user_id = payload['id']
        print(user_id)


        print(expense_id)
        print(pay_amt)
        print(receive)
        print(id)
        pay_obj = get_object_or_404(Debts, exp_id=expense_id, group_id=id, payer=user_id, bearer=receive)
        print(3)
        if pay_amt == pay_obj.amt:
            pay_obj.is_paid = True
        elif pay_amt < pay_obj.amt:
            pay_obj.amt -= pay_amt
        else:
            return Response("Enter the Correct Amount")
        update_user_balance(expense_id, user_id, receive, pay_amt)
        pay_obj.save()

# class InviteCreate(DetailView):
#
#     def get_queryset(self):
#         return self.request.
# # Create your views here.

# class GroupsList(APIView):
#     def get(self, request):
#         queryset = Group.objects.all()
#         serializer = GroupSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = GroupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class GroupDetails(APIView):
#     def get(self, request, id):
#         group = get_object_or_404(Group, pk=id)
#         serializer = GroupSerializer(group)
#         return Response(serializer.data)

#     def put(self, request, id):
#         group = get_object_or_404(Group, pk=id)
#         serializer = GroupSerializer(group, data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         group = get_object_or_404(Group, pk=id)
#         group.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class GroupUsersList(APIView):
#     def get(self, request, id):
#         queryset = GroupToUser.objects.filter(group_id=id)
#         serializer = GroupToUserSerializer(queryset, many=True)
#         return Response(serializer.data)


# class AddUserToGroup(APIView):
#     def post(self, request):
#         serializer = GroupToUserSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data)
