from datetime import datetime

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify
from notes.models import Notes, Category, TagPost

menu = [{'title': "Поиск заметки", 'url_name': 'find'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "Новая заметка", 'url_name': 'add'},
        {'title': "О сайте", 'url_name': 'about'},
        ]

cats_db = [
    {'id': 1, 'name': 'Расписание'},
    {'id': 2, 'name': 'Списки'},
    {'id': 3, 'name': 'Прочие заметки'},
]


def index(request):
    posts = Notes.private.all().order_by('-time_update')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'notes/index.html',
                  context=data)


def categories(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Notes.private.filter(cat_id=category.pk)
    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'notes/cats.html',
                  context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Notes.Status.PRIVATE)
    data = {
    'title': f'Тег: {tag.tag}',
    'menu': menu,
    'posts': posts,
    'cat_selected': None,
    }
    return render(request, 'notes/index.html',
    context=data)


def archive(request, year):
    data = {
        'title': 'Архив до года ' + str(year),
        'menu': menu,
        'posts': Notes.private.all().filter(time_create__lte=datetime(year, 1, 1)),
    }
    return render(request, 'notes/index.html',
                  context=data)



def show_post(request, post_slug):
    post = get_object_or_404(Notes, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'notes/post.html',
                  context=data)



def about(request):
    return render(request, 'notes/about.html',
                  {'title': 'О сайте', 'menu': menu})


def find(request):
    data = {
        'title': 'Найти заметку',
        'menu': menu,
        'posts': Notes.objects.all(),
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'notes/find.html',
                  context=data)


def login(request):
    return render(request, 'notes/login.html',
                  {'title': 'Вход', 'menu': menu})


def create(request):
    if request.method == "POST":
        note = Notes()
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, "notes/create.html")


# изменение данных в бд
def edit(request, post_slug):
    try:
        note = Notes.objects.get(slug=post_slug)
        if request.method == "POST":
            note.title = request.POST.get("title")
            note.content = request.POST.get("content")
            note.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "notes/edit.html", {"post": note})
    except Notes.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")


# удаление данных из бд
def delete(request, post_slug):
    try:
        note = Notes.objects.get(slug=post_slug)
        note.delete()
        return HttpResponseRedirect("/")
    except Notes.DoesNotExist:
        return HttpResponseNotFound("<h2>Note not found</h2>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
