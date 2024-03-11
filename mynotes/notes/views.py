from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify

menu = [{'title': "Поиск заметки", 'url_name': 'find'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "Новая заметка", 'url_name': 'add'},
        {'title': "О сайте", 'url_name': 'about'},
        ]

notes = [
    {'id': 1,
     'title': '10.01.2024',
     'content': '1. Проснуться <br> 2. Улыбнуться',
     'is_published': True,
     'category': 1},
    {'id': 2,
     'title': '11.01.2023',
     'content': '1. Лечь спать <br> 2. Расстроиться',
     'is_published': True,
     'category': 1},
    {'id': 3,
     'title': 'Продукты',
     'content': '1. Молоко <br> 2. Сыр <br> 3. Яйца',
     'is_published': True,
     'category': 2},
    {'id': 4,
     'title': 'Дела на завтра',
     'content': '1. Сходить к врачу <br> 2. Приготовить кушать <br> 3. Прирать комнату',
     'is_published': True,
     'category': 2},
    {'id': 5,
     'title': 'Адрес',
     'content': 'ул.Блюхера 32/1',
     'is_published': True,
     'category': 3},
]

cats_db = [
    {'id': 1, 'name': 'Расписание'},
    {'id': 2, 'name': 'Списки'},
    {'id': 3, 'name': 'Прочие заметки'},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': notes,
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'notes/index.html',
                  context=data)


def categories(request, cat_id):
    data = {
        'title': 'Фильтр заметок',
        'menu': menu,
        'posts': notes,
        'cat_selected': cat_id,
    }
    return render(request, 'notes/cats.html',
                  context=data)

def archive(request, year):
    if year > 2024:
        # raise Http404()
        # return redirect('home', permanent=True)
        return HttpResponseRedirect('/')
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def show_post(request, post_id):
    return HttpResponse(f"Отображение заметки с id = {post_id}")

def add_notes(request):
    return render(request, 'notes/add.html',
                  {'title': 'Новая заметка', 'menu': menu})

def about(request):
    return render(request, 'notes/about.html',
                  {'title': 'О сайте', 'menu': menu})


def find(request):
    data = {
        'title': 'Найти заметку',
        'menu': menu,
        'posts': notes,
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'notes/find.html',
                  context=data)


def login(request):
    return render(request, 'notes/login.html',
                  {'title': 'Вход', 'menu': menu})





def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
