from django.db import models
from authentication.models import User
from .leave import Leave

class LeaveApproval(models.Model):
    leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='approval')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_leaves')
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval for {self.leave} by {self.approver}" 