from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_name', 'group_id', 'payee_id', 'total_amount']


@admin.register(models.ExpenseToUser)
class ExpenseToUserAdmin(admin.ModelAdmin):
    list_display = ['expense_id', 'users_id', 'amount_paid']
