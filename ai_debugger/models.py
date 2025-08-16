from django.db import models
from django.contrib.auth.models import User

class AIAnalysisRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    code = models.TextField()
    language = models.CharField(max_length=50)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    results = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Analysis Request by {self.submitted_by.username} ({self.language})"