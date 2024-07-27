from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categorylist, name="categorylist"),
    path("removeWachlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWachlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("seeWachlist", views.seeWatchlist, name="seeWatchlist"),
    path("addCommment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>",views.addBid, name="addBid"),
    path("closeListing/<int:id>",views.closeListing, name="closeListing"),
]
