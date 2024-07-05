from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator


class Task(models.Model):
    created_by = models.ForeignKey(CustomUser, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)

    name = models.CharField(max_length=255, default="Nameless Task", blank=True)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

