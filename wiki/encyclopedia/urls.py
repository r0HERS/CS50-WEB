from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("createnewpage",views.createnewpage, name="createnewpage"),
    path("editpage/",views.editpage, name="editpage"),
    path("saveedit/",views.saveedit, name="saveedit"),
    path("randpage/",views.randpage, name="randpage"),
]
