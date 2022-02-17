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
    name = models.CharField(max_length=1024)
    group_type = models.CharField(max_length=1, choices=GROUP_TYPE_CHOICES, default=GROUP_HOME)
    description = models.TextField()
    created_at = models.DateField(auto_now=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)

    def __dir__(self) -> str:
        return self.name

    class Meta:
        ordering =['name']


class GroupToUser(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.group_id) + "-" + str(self.user_id)

    class Meta:
        unique_together = ('group_id', 'user_id')
