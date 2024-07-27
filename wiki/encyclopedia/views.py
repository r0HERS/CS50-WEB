from django.shortcuts import render,redirect
import markdown2
from django.http import HttpResponse
import random

from . import util


def transform(title):
    markdownpage = util.get_entry(title)
    
    if markdownpage == None:
        return None
    else:
        htmlpage = markdown2.markdown(markdownpage)
        return htmlpage

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def title(request,title):

    htmlpage = transform(title)

    if htmlpage == None:

        return render(request, "encyclopedia/notfound.html",{
            "title":title.capitalize(),
            "text": "not found"
        })
    
    else:

        return render(request, "encyclopedia/title.html",{
            "title":title.capitalize(),
            "body": htmlpage
        })
    
def search(request):
    if request.method == "POST":

        querry = request.POST['q']
        entries = util.list_entries()

        
        for entry in entries:
            if querry.lower() in entry.lower():
                htmlpage = transform(querry)

                if htmlpage is not None:
                    return render(request, "encyclopedia/title.html",{
                    "title":querry.capitalize(),
                    "body": htmlpage
                })
        else:
            results = []
            for entry in entries:
                if querry.lower() in entry.lower():
                    results.append(entry.capitalize())


            return render(request, "encyclopedia/search_results.html",{
                "title": querry,
                "results": results
            })

def createnewpage(request):
    if request.method == "GET":
        return render(request,"encyclopedia/createnewpage.html")
    else:
        title = request.POST['name']
        page_exist = util.get_entry(title)
        content = request.POST['markdownbody']
        
        if not title: 
            return render(request, "encyclopedia/notfound.html", {
                "title": "Error",
                "text": "No title input."
            })

        if page_exist is not None:
                return render(request, "encyclopedia/notfound.html",{
                "title":title.capitalize(),
                "text": "page already exist"
            })
        else:
                
                util.save_entry(title,content)
                htmlbody=transform(title)

                return render(request, "encyclopedia/title.html",{
                    "title":title.capitalize(),
                    "body": htmlbody
                })
    
def editpage(request):
    if request.method == "POST":
        title = request.POST['title']
        markdowncontent = util.get_entry(title)
        return render(request,"encyclopedia/editpage.html",{
        "title": title,
        "markdowncontent": markdowncontent
        })
    
def saveedit(request):
    if request.method == "POST":
        title = request.POST['name']
        markdowncontent = request.POST['markdownbody']
        
        util.save_entry(title,markdowncontent)

        htmlbody=transform(title)

        return render(request, "encyclopedia/title.html",{
                "title":title.capitalize(),
                "body": htmlbody
        })
def randpage(request):

    entries = util.list_entries()
    num = len(entries)
    rand = random.random()*100

    chosen=rand%num

    title=entries[int(chosen)]
    htmlpage = transform(title)


    return render(request, "encyclopedia/title.html",{
                "title":title.capitalize(),
                "body": htmlpage
        })