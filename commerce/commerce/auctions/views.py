from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Listing, Category, Comments, Bid


def index(request):

    avaiablelistings = Listing.objects.filter(isActive=True)


    return render(request, "auctions/index.html",{
        "listings": avaiablelistings,
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def addlisting(request):
    if request.method == "GET":
        return render(request, "auctions/addlisting.html", {
            "categories": Category.objects.all()
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category_id = request.POST["category"]
        owner_name = request.POST["user"]

        try:
            category = Category.objects.get(id=category_id)
            owner = User.objects.get(username=owner_name)

            bid = Bid(
                user = owner,
                value = float(price),
            )

            bid.save()

            listing = Listing.objects.create(
                title=title,
                description=description,
                image=image,
                price=bid,
                category=category,
                owner=owner
            )

            listing.save()

            return render(request,"auctions/addlisting.html",{
                "message": "Listing created succesfully.",
                "categories": Category.objects.all()
            })
        except IntegrityError:
            return render(request, "auctions/addlisting.html", {
                "message": "ERROR.",
                "categories": Category.objects.all()
            })
        
def listing(request,listing_id):
    listing = Listing.objects.get(id=listing_id)

    comments = Comments.objects.filter(listing=listing)

    inWatchlist = request.user in listing.watchlist.all()

    user = request.user

    return render(request,"auctions/listing.html",{
                "listing": listing,
                "inwatchlist": inWatchlist,
                "comments": comments,
            })

def categories(request):
    return render(request, "auctions/categories.html", {
            "categories": Category.objects.all()
        })

def categorylist(request,category_id):
    category = Category.objects.get(id=category_id)
    listings = Listing.objects.filter(category = category, isActive = True)
    return render(request,"auctions/index.html",{
                "listings": listings
            })

def removeWatchlist(request,id):

    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request,id):

    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.add(user)

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def seeWatchlist(request):

    user = request.user

    listing = user.watchlist.all()

    return render(request,"auctions/index.html",{
                "listings": listing
            })

def addComment(request,id):

    comment = request.POST["comment"]
    comment_user = request.user
    comment_listing = Listing.objects.get(pk = id)

    newcomment = Comments.objects.create(

        user = comment_user,
        listing = comment_listing,
        text = comment,

    )

    newcomment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request,id):
    bid_listing = Listing.objects.get(pk = id)

    comments = Comments.objects.filter(listing=bid_listing)
    inWatchlist = request.user in bid_listing.watchlist.all()
    
    curret_bid = bid_listing.price.value
    bid = float(request.POST["bid"])
    bid_user = request.user

    
    
    if bid > curret_bid:

        newbid = Bid.objects.create(
            value = bid,
            user = bid_user,
        )
        newbid.save()

        bid_listing.price = newbid

        bid_listing.save()

       
        
        return render(request,"auctions/listing.html",{
                "message": "Successfull Bid.",
                "listing": bid_listing,
                "inwatchlist": inWatchlist,
                "comments": comments,

            })

    else:

        return render(request,"auctions/listing.html",{
                "message": "Something went wrong.",
                "listing": bid_listing,
                "inwatchlist": inWatchlist,
                "comments": comments,
            })

def closeListing(request,id):

    listing = Listing.objects.get(pk = id)

    listing.isActive = False

    listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))