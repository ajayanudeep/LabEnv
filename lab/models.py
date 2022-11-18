from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClassRoom(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    subject = models.CharField(max_length=200)
    classname = models.CharField(max_length=10)
    students = models.ManyToManyField(User,related_name="participants",blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.subject+" "+self.classname

class Assignment(models.Model):
    class_in = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    type = models.CharField(max_length=100,default="Question")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True)
    due_time = models.TimeField(default=False,blank=True)
    status = models.IntegerField(default=1,blank=True)
    question = models.TextField(max_length=500)

    class Meta:
        ordering = ['-updated', '-created']

class Answer(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

