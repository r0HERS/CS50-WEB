from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Project(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_projects')
    members = models.ManyToManyField(User, blank=True, null=True, related_name="members")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Invite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter')
    invite_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited')
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.invited_by} invited {self.invite_to} to {self.project}"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_task')
    members = models.ManyToManyField(User, blank=True, null=True, related_name="members_task")
    complete = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=250)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    time = models.IntegerField()

    def __str__(self):
        return f"{self.title} is a task of {self.project} due {self.due_date}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "comment_user")
    task = models.ForeignKey(Task, on_delete = models.CASCADE, blank = True, null = True, related_name = "comment_task")
    project = models.ForeignKey(Project, on_delete = models.CASCADE, blank = True, null = True, related_name = "comment_Project")
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} comment on {self.task} of {self.project}"
