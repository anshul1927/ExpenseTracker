from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from groups.models import Group
from users.models import User
from .models import Expense, ExpenseToUser, Debts
from .serializers import ExpenseSerializer, ExpenseToUserSerializer


# Create your views here.
def get_debts(shared_btw_users, payers):
    dict = {}
    for payer in payers:
        amt = payers[payer]
        share = float(amt / len(shared_btw_users))
        for user in shared_btw_users:
            if user != payer:
                dict[(user, payer)] = share

    return dict


def add_expense_to_user(expense_id, list_of_user, total_amt, payers):
    share = float(total_amt / len(list_of_user))
    for user in list_of_user:
        exp_to_usr = ExpenseToUser(expense_id=get_object_or_404(Expense, pk=expense_id),
                                   users_id=get_object_or_404(User, pk=user),
                                   share=share,
                                   initial_amt_paid=payers.get(user, 0),
                                   outstanding=payers.get(user, 0) - share)
        exp_to_usr.save()


def add_users_debt(debts, expense_id, group_id):
    for debt in debts:
        user_debt = Debts(exp_id=get_object_or_404(Expense, pk=expense_id),
                          group_id=get_object_or_404(Group, pk=group_id),
                          payer=get_object_or_404(User, pk=debt[0]),
                          bearer=get_object_or_404(User, pk=debt[1]),
                          amt=debts[debt])
        user_debt.save()


class ExpenseList(APIView):
    def get(self, request, id):
        queryset = Expense.objects.filter(group_id=id)
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        data_dict = request.data
        shared_btw_users = data_dict.pop('user_list')
        payers = data_dict.pop('payers')
        payers = {int(k): v for k, v in payers.items()}
        debts = get_debts(shared_btw_users, payers)
        serializer = ExpenseSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        add_expense_to_user(serializer.data['id'], shared_btw_users,
                            data_dict['total_amount'],
                            payers)
        add_users_debt(debts, serializer.data['id'], serializer.data['group_id'])
        return Response(serializer.data)


class ExpenseUsers(APIView):
    def get(self, request, id):
        queryset = ExpenseToUser.objects.filter(expense_id=id)
        serializer = ExpenseToUserSerializer(queryset, many=True)
        return Response(serializer.data)


def update_user_balance(expense_id, sender, reciever, amt):
    bal_obj = get_object_or_404(ExpenseToUser, expense_id=expense_id, payer=sender, bearer=reciever)
    bal_obj.amt_paid += amt
    bal_obj.outstanding += amt
    bal_obj.save()
    bal_obj = get_object_or_404(ExpenseToUser, expense_id=expense_id, payer=reciever, bearer=sender)
    bal_obj.amt_receive += amt
    bal_obj.outstanding -= amt
    bal_obj.save()
