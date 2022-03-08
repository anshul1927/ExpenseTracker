from django.db import models

# Create your models here.
from groups.models import Group
from users.models import User


class Expense(models.Model):
    expense_name = models.CharField(max_length=255)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class ExpenseToUser(models.Model):
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_user')
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    initial_amt_paid = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    amt_receive = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    amt_paid = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    outstanding = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class Debts(models.Model):
    exp_id = models.ForeignKey(Expense, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payer')
    bearer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bearer')
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
