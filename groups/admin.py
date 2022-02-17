from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_type', 'description', 'created_at', 'created_by']
    list_per_page = 10

@admin.register(models.GroupToUser)
class GroupToUserAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'user_id']