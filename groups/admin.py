from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_type', 'group_description', 'created_at','deleted_at', 'created_by','is_active']


#admin.site.register(models.Group)

admin.site.register(models.GroupToUser)
# @admin.register(models.GroupToUser)
# class GroupToUserAdmin(admin.ModelAdmin):
#     list_display = ['group_id', 'user_id','is_active']