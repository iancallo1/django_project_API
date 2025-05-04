from django.db import models

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_days = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name 