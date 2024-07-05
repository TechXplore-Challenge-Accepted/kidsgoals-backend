from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator


class Task(models.Model):
    created_by = models.ForeignKey(CustomUser, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='tasks', on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Goal(models.Model):
    kid = models.OneToOneField(CustomUser, related_name='goal', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_achieved = models.BooleanField(default=False)

    @property
    def progress(self):
        if self.price == 0:
            return 0
        return round(min(100, self.kid.balance / self.price * 100), 2)

    def __str__(self):
        return f"{self.name} - {'Achieved' if self.is_achieved else 'Not Achieved'}"
