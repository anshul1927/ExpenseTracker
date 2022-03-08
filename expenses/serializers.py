from rest_framework import serializers
from .models import Expense, ExpenseToUser, Debts


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class ExpenseToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseToUser
        fields = "__all__"


class DebtsSerializer(serializers.ModelSerializer):
    remaining_debt = serializers.SerializerMethodField()

    def get_remaining_debt(self, debt_obj: Debts):
        return debt_obj.debt - debt_obj.amt_paid

    class Meta:
        model = Debts
        fields = ['id', 'exp_id', 'group_id', 'payer', 'bearer',  'amt_paid', 'remaining_debt']
