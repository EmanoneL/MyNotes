from datetime import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from notes.forms import AddNoteForm, UploadFileForm
from notes.models import Notes, Category, TagPost, UploadFiles
from notes.utils import DataMixin

menu = [{'title': "Поиск заметки", 'url_name': 'find'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "Новая заметка", 'url_name': 'add'},
        {'title': "О сайте", 'url_name': 'about'},
        ]



# class Create(View):
#     def get(self, request):
#         form = AddNoteForm()
#         return render(request, "notes/create.html",
#                       {'title': 'Добавление статьи',
#                        'form': form
#                        }
#                       )
#
#     def post(self, request):
#         form = AddNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
# class Create(FormView):
#     form_class = AddNoteForm
#     template_name = 'notes/create.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class Create(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddNoteForm
    template_name = 'notes/create.html'
    title_page = 'Добавление заметки'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class MyNotes(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'notes/my_notes.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Фильтруем записи по автору, который совпадает с текущим пользователем
        return Notes.private.filter(author=self.request.user).select_related('cat').order_by('-time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        # Добавляем дополнительный контекст
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(context, title='Мои заметки', cat_selected=0)
        return mixin_context

class NotesHome(DataMixin, ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'


    def get_queryset(self):
        print(Notes.published.all())
        return Notes.published.all().select_related('cat').order_by('-time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='Главная страница', cat_selected=0)


class NotesCategory(DataMixin,ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Notes.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория-' + cat.name, cat_selected=cat.id, )


class TagPostList(DataMixin,ListView):
    template_name = 'notes/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег ' + tag.tag)

    def get_queryset(self):
        return Notes.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Notes
    template_name = 'notes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])
    def get_object(self, queryset=None):
        return get_object_or_404(Notes.private.filter(author=self.request.user),
                                 slug=self.kwargs[self.slug_url_kwarg])


class UpdatePage(DataMixin,UpdateView):
    model = Notes
    fields = ['title', 'content', 'picture', 'is_published', 'cat']
    template_name = 'notes/create.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование заметки'



class DeleteNote(DataMixin, DeleteView):
    model = Notes
    template_name = 'notes/delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление заметки'
    extra_context = {
        'menu': menu,
        'title': 'Удаление статьи',
    }


def archive(request, year):
    data = {
        'title': 'Архив до года ' + str(year),
        'menu': menu,
        'posts': Notes.private.all().filter(time_create__lte=datetime(year, 1, 1)),
    }
    return render(request, 'notes/index.html',
                  context=data)


def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())

    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def about(request):
    contact_list = Notes.private.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes/about.html', {'page_obj':
                                                    page_obj, 'title': 'О сайте'})


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
    pass


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
