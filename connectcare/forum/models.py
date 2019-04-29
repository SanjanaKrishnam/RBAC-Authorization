from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-timestamp"]

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name='comments',on_delete=models.CASCADE,)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


