from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_name', 'group_id', 'created_by', 'total_amount']


@admin.register(models.ExpenseToUser)
class ExpenseToUserAdmin(admin.ModelAdmin):
    list_display = ['expense_id', 'users_id', 'initial_amt_paid', 'amt_receive', 'amt_paid', 'outstanding']


@admin.register(models.Debts)
class DebtsAdmin(admin.ModelAdmin):
    list_display = ['exp_id', 'group_id', 'payer', 'bearer', 'debt', 'amt_paid', 'is_paid']
