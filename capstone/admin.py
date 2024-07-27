from django.contrib import admin

from .models import User, Project,Invite,Task,Comments

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Invite)
admin.site.register(Task)
admin.site.register(Comments)