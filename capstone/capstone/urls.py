from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_project", views.create_project, name="create_project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
    path("project/<int:id>", views.project, name="project"),
    path("invite/<int:id>", views.invite, name="invite"),
    path("accept_invite/<int:id>", views.accept_invite, name="accept_invite"),
    path("decline_invite/<int:id>", views.decline_invite, name="decline_invite"),
    path("add_task/<int:id>", views.add_task, name="add_task"),
    path("edit_task/<int:id>", views.edit_task, name="edit_task"),
    path("complete_task/<int:id>", views.complete_task, name="complete_task"),
    path("delete_task/<int:id>", views.delete_task, name="delete_task"),
    path("get_events/<int:id>",views.get_events, name="get_events"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
]
