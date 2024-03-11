from django.urls import path, re_path, register_converter
from notes import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('categories/<int:cat_id>/', views.categories, name='categories'),
    path('archive/<year4:year>/', views.archive, name='archive'),

    path('find/', views.find, name='find'),
    path('add/', views.add_notes, name='add'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.show_post,
         name='post'),


]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
