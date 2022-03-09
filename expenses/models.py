from django.db import models

# Create your models here.
from groups.models import Group
from users.models import User


class Expense(models.Model):
    expense_name = models.CharField(max_length=255)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.total_amount = round(self.total_amount, 2)
        super(Expense, self).save(*args, **kwargs)


class ExpenseToUser(models.Model):
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='expense_user')
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.FloatField(default=0.0)
    initial_amt_paid = models.FloatField(default=0.0)
    amt_receive = models.FloatField(default=0.0)
    amt_paid = models.FloatField(default=0.0)
    outstanding = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.share = round(self.share, 2)
        self.initial_amt_paid = round(self.initial_amt_paid, 2)
        self.amt_receive = round(self.amt_receive, 2)
        self.amt_paid = round(self.amt_paid, 2)
        self.outstanding = round(self.outstanding, 2)
        super(ExpenseToUser, self).save(*args, **kwargs)



class Debts(models.Model):
    exp_id = models.ForeignKey(Expense, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payer')
    bearer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bearer')
    debt = models.FloatField()
    amt_paid = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.debt = round(self.debt, 2)
        self.amt_paid = round(self.amt_paid, 2)
        self.is_paid = round(self.is_paid, 2)
        super(Debts, self).save(*args, **kwargs)
