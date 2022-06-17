from django.db import models
from django.contrib.auth.models import User


class Protocol(models.Model):
    title = models.CharField(max_length=50)
    abst = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Process(models.Model):
    title= models.CharField(max_length=100)
    content= models.TextField(null=True, blank=True)
    time= models.DurationField(null=True, blank=True)
    sub= models.BooleanField(default=False)
    rank= models.IntegerField(default=0)
    protocol= models.ForeignKey(Protocol, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



