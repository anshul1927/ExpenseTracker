from django.db import models
from users.models import User


# Create your models here.


class Group(models.Model):
    GROUP_HOME = 'H'
    GROUP_TRIP = 'T'
    GROUP_OTHER = 'O'

    GROUP_TYPE_CHOICES = [
        (GROUP_HOME, 'HOME'),
        (GROUP_TRIP, 'TRIP'),
        (GROUP_OTHER, 'OTHER'),
    ]
    group_name = models.CharField(max_length=45, blank=True, null=True)
    group_type = models.CharField(max_length=1, choices=GROUP_TYPE_CHOICES, default=GROUP_HOME)
    group_description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User,db_column='created_by', unique=False, on_delete=models.CASCADE)
    is_active = models.IntegerField(blank=True, null=True)

    def __dir__(self) -> str:
        return self.group_name

    class Meta:
        unique_together = ['group_name', 'created_by']
        ordering = ['group_name']


class GroupToUser(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.group_id) + "-" + str(self.user_id)

    class Meta:
        unique_together = ('group_id', 'user_id')
