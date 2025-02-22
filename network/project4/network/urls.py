
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following_page, name="following"),
    path("edit_post/<int:id>", views.edit_post, name="edit_post"),
    path("like/<int:id>", views.like, name="like"),
    path("unlike/<int:id>", views.unlike, name="unlike"),
]
