from django.db import models

# Create your models here.
from groups.models import Group
from users.models import User


class Expense(models.Model):
    expense_name = models.CharField(max_length=255)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    payee_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class ExpenseToUser(models.Model):
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE)
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
