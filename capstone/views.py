from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User,Project,Invite,Task,Comments

def index(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_projects = Project.objects.filter(Q(owner=current_user) | Q(members=current_user)).distinct()
        inbox_invites = Invite.objects.filter(invite_to = current_user, accepted = False)

        return render(request, 'capstone/index.html', {
            "user_projects": user_projects,
            "invites": inbox_invites,
        })
    else:
        return render(request, 'capstone/index.html')

@login_required
def project(request,id):

    current_user = request.user
    project = Project.objects.get(pk = id)
    members = project.members.all()
    all_users = User.objects.all()
    inbox_invites = Invite.objects.filter(invite_to = current_user, accepted = False)

    all_tasks = Task.objects.filter(project = project)

    current_date = datetime.now().date()

    for task in all_tasks:
        task.overdue = task.due_date < current_date

    completed_tasks = all_tasks.filter(complete = True)

    total_tasks = all_tasks.count()
    completed_tasks_count = completed_tasks.count()

    if total_tasks == 0:
        completion_percentage = 0
    else:
        completion_percentage = (completed_tasks_count / total_tasks) * 100
        completion_percentage = round(completion_percentage, 2)

    comments = Comments.objects.all()

    return render(request, 'capstone/project.html',{
        "project": project,
        "all_users": all_users,
        "invites": inbox_invites,
        "members": members,
        "all_tasks": all_tasks,
        "completion_percentage": completion_percentage,
        "comments": comments,
    })

def add_comment(request,id):

    task = Task.objects.get(pk = id)
    project = task.project
    comment = request.POST["comment"]
    comment_user = request.user

    newcomment = Comments.objects.create(
        user = comment_user,
        task = task,
        text = comment,
        project = task.project,
    )

    newcomment.save()

    return HttpResponseRedirect(reverse("project", args=(project.id, )))

def add_task(request,id):

    project = Project.objects.get(pk = id)

    title = request.POST["title"]

    start_date = request.POST["start_date"]

    due_date = request.POST["due_date"]

    description = request.POST["description"]

    time = request.POST["time"]
    members_ids = request.POST.getlist('taskMembers')

    new_task = Task.objects.create(
            project = project,
            title = title,
            description = description,
            start_date = start_date,
            due_date = due_date,
            time = time,
        )

    for member_id in members_ids:
        user = User.objects.get(pk=member_id)
        new_task.members.add(user)

    return HttpResponseRedirect(reverse("project", args=(id, )))

@csrf_exempt
def edit_task(request,id):

    task = Task.objects.get(pk = id)
    data = json.loads(request.body)

    newTitle = data.get('title')
    newDescription = data.get('description')
    newTime = data.get('time')
    newStart = data.get('start_date')
    newDue = data.get('due_date')

    task.title = newTitle
    task.time = newTime
    task.description = newDescription
    task.start_date = newStart
    task.due_date = newDue

    task.save()

    return JsonResponse({'status': 'success'})

@csrf_exempt
def complete_task(request,id):

    task = Task.objects.get(pk = id)

    task.complete = True

    task.save()

    return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_task(request,id):

    task = Task.objects.get(pk = id)

    task.delete()

    return JsonResponse({'status': 'success'})

@csrf_exempt
def invite(request,id):

    invited_by = request.user
    invite_to = User.objects.get(pk = id)
    data= json.loads(request.body)
    project_id = data.get('project_id')
    project = Project.objects.get(pk = project_id)

    if invite_to:
        
        new_invite = Invite(
            project = project,
            invited_by = invited_by,
            invite_to = invite_to,
        )

        new_invite.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'No user  selected.'}, status=400)


@login_required
def create_project(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        description = request.POST["description"]

        new_project = Project(
            name=name,
            description=description,
            owner=current_user
        )
        new_project.save()

        new_project.members.add(current_user)

        return HttpResponseRedirect(reverse("index"))
    else:
        current_user = request.user
        inbox_invites = Invite.objects.filter(invite_to = current_user, accepted = False)
        return render(request,'capstone/create_project.html',{
                "invites": inbox_invites,
        })

@csrf_exempt
def delete_project(request,id):

    project = Project.objects.get(pk = id)

    project.delete()

    return JsonResponse({'status': 'success'})


def get_events(request,id):
    project = Project.objects.get(pk = id)
    tasks = Task.objects.filter(project = project)
    events = []
    i=0
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFF5']

    current_date = datetime.now().date()
    for task in tasks:
        i = i + 1
        end_date = task.due_date + timedelta(days=1)
        overdue = task.due_date < current_date
        color = colors[i % len(colors)]
        if overdue:
            color = '#FF0000'
        if not task.complete:
            events.append({
                'id': task.id,
                'title': task.title,
                'start': task.start_date.isoformat(), 
                'end': end_date.isoformat(),  
                'description': task.description,
                'time': task.time, 
                'color': color,
                'overdue': overdue
            })

    return JsonResponse(events, safe=False)
    


@csrf_exempt
def accept_invite(request,id):

    current_user = request.user

    invite = Invite.objects.get(pk = id)

    invite.accepted = True

    invite.save()

    project_id = invite.project.id

    project = Project.objects.get(pk = project_id)

    project.members.add(current_user)

    return JsonResponse({'status': 'success'})

@csrf_exempt
def decline_invite(request,id):

    current_user = request.user

    invite = Invite.objects.get(pk = id)

    invite.delete()

    return JsonResponse({'status': 'success'})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
    