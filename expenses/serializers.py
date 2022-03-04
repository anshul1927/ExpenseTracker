from rest_framework import serializers
from .models import Expense, ExpenseToUser


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"



class ExpenseToUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseToUser
        fields = "__all__"
