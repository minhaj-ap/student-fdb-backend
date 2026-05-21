
from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('academics', 'Academics'),
        ('infrastructure', 'Infrastructure'),
        ('activities', 'Activities'),
        ('other', 'Other')
    ])
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"