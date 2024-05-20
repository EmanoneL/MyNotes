from django.urls import path, re_path, register_converter
from notes import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.NotesHome.as_view(), name='home'),
    path('categories/<slug:cat_slug>/', views.NotesCategory.as_view(), name='categories'),
    path('archive/<year4:year>/', views.archive, name='archive'),

    path('find/', views.find, name='find'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('create/', views.Create.as_view(), name='create'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit'),
    path('delete/<slug:slug>/', views.DeleteNote.as_view(), name='delete'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),


]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
