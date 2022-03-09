from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from groups.models import Group
from users.models import User
from .minimum import minCashFlow
from .models import Expense, ExpenseToUser, Debts
from .serializers import ExpenseSerializer, ExpenseToUserSerializer


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
                          debt=debts[debt])
        user_debt.save()


def get_user_dict(id):
    return None


def get_debts_graph_arr(debts, total_members_in_expesne, user_index):
    debts_list = list(debts.items())
    rows, cols = (total_members_in_expesne, total_members_in_expesne)
    arr = [[0] * cols for _ in range(rows)]

    lis = list(debts.keys())
    # print(debts)
    # print(total_members_in_expesne)
    # print(user_index)
    # print(lis)
    for i in range(len(debts)):
        r = user_index.get(lis[i][0])
        c = user_index.get(lis[i][1])
        # print("r :- ", r, " c :- ", c, " type(list[i] :- ", type(lis[i]))
        arr[r][c] = debts.get(lis[i])
    return arr


def simplify_debts(debts, shared_btw_users):
    user_index = {}
    for i in range(len(shared_btw_users)):
        user_index[shared_btw_users[i]] = i

    arr = get_debts_graph_arr(debts, len(shared_btw_users), user_index)

    final_debts = minCashFlow(arr, len(shared_btw_users))
    # print(final_debts)

    new_debts = {}
    final_debts_keys = list(final_debts.keys())
    user_index_key_list = list(user_index.keys())
    user_index_value_list = list(user_index.values())

    for i in range(len(final_debts)):
        temp = final_debts_keys[i]
        print(temp)
        pos1 = user_index_value_list.index(temp[0])
        pos2 = user_index_value_list.index(temp[1])
        new_debts[(user_index_key_list[pos1], user_index_key_list[pos2])] = final_debts.get(final_debts_keys[i])

    # print(new_debts)
    return new_debts


class ExpenseList(APIView):
    def get(self, request, id):
        queryset = Expense.objects.filter(group_id=id)
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        data_dict = request.data
        # print(data_dict)
        shared_btw_users = data_dict.pop('user_list')
        payers = data_dict.pop('payers')
        payers = {int(k): v for k, v in payers.items()}
        debts = get_debts(shared_btw_users, payers)
        new_debts = simplify_debts(debts, shared_btw_users)

        serializer = ExpenseSerializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        add_expense_to_user(serializer.data['id'], shared_btw_users,
                            data_dict['total_amount'],
                            payers)
        add_users_debt(new_debts, serializer.data['id'], serializer.data['group_id'])

        return Response(serializer.data)


class ExpenseUsers(APIView):
    def get(self, request, id):
        queryset = ExpenseToUser.objects.filter(expense_id=id)
        serializer = ExpenseToUserSerializer(queryset, many=True)
        return Response(serializer.data)


def update_user_balance(expense_id, sender, reciever, amt):
    bal_obj = get_object_or_404(ExpenseToUser, expense_id=expense_id, users_id=sender)
    bal_obj.amt_paid = bal_obj.amt_paid +  amt
    bal_obj.outstanding = bal_obj.outstanding + amt
    bal_obj.save()
    bal_obj = get_object_or_404(ExpenseToUser, expense_id=expense_id, users_id=reciever)
    bal_obj.amt_receive = bal_obj.amt_receive + amt
    bal_obj.outstanding = bal_obj.outstanding - amt
    bal_obj.save()
