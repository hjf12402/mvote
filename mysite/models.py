from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    male = models.BooleanField(default=True)

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PollItem(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    image_url = models.URLField(null=True, blank=True)
    vote = models.PositiveIntegerField(default=0)

class VoteCheck(models.Model):
    userid = models.PositiveIntegerField()
    pollid = models.PositiveIntegerField()
    vote_date = models.DateField(auto_now_add=True)