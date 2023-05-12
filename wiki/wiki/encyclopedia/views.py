import random
from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from . import util

def index(request):
    return render(request,"encyclopedia/index.html", {
        "entries": util.list_entries(),
        "page": "All Pages"
    }) 

def displayer(request,title):  
    markdowner=Markdown()
    if util.get_entry(title) is None:
        return render(request,"encyclopedia/entry.html",{
            "content":f"error: requested \"{title}\"- page was not found"
        }) 
    return render(request,"encyclopedia/entry.html",{
        "title":title,
        "content":markdowner.convert(util.get_entry(title)),
    })
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        if util.get_entry(entry_search) is None:
            content=None
        else:
            content = Markdown().convert(util.get_entry(entry_search))
        if content is not None:
            return render(request,"encyclopedia/entry.html",{
                "title":entry_search,
                "content":content
            })
        else:
            all_entries=util.list_entries()
            results = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    results.append(entry)
            return render(request,"encyclopedia/search.html",{
                "results":results
            })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        is_title_exist = util.get_entry(title)
        if is_title_exist is not None:
            return render(request,"encyclopedia/entry.html",{
                "content":f"error: Entry already exists"
            })
        else:
            util.save_entry(title,content)
            converted_html = Markdown().convert(util.get_entry(title))
            return render(request,"encyclopedia/entry.html",{
                "title":title,
                "content":converted_html
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content 
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content'] #bu content markdown content, renderdaki contente atamadan once bunu html'e cevirmek lazim
        util.save_entry(title,content)
        converted_html = Markdown().convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":converted_html
        })
def random_page(request):
    all_entries=util.list_entries()
    title_of_random=random.choice(all_entries)
    converted_html=Markdown().convert(util.get_entry(title_of_random))
    return render(request,"encyclopedia/entry.html",{
        "title":title_of_random,
        "content":converted_html
    })
