from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone

from .models import Notes, TagPost, FootNote, Category


class DateRangeFilter(SimpleListFilter):
    title = 'date range'
    parameter_name = 'time_create'

    def lookups(self, request, model_admin):
        now = timezone.now()
        one_week_ago = now - timedelta(weeks=1)
        one_day_ago = now - timedelta(days=1)
        return [
            (f'{one_week_ago.date() - now.date()}', 'Last week'),
            (f'{one_day_ago.date() - now.date()}', 'Last day'),

        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        one_week_ago = now - timedelta(weeks=1)
        one_day_ago = now - timedelta(days=1)

        if self.value() >= one_week_ago:
            return queryset.filter(time_create__range=(one_week_ago, now))

        if self.value() >= one_day_ago:
            return queryset.filter(time_create__range=(one_day_ago, now))

class IsPublishedFilter(admin.SimpleListFilter):
    title = 'Опубликовано'
    parameter_name = 'is_published'

    def lookups(self, request, model_admin):
        return [
            ({Notes.Status.PRIVATE}, 'Личное'),
            ({Notes.Status.PUBLISHED}, 'Опубликовано'),
        ]

    def queryset(self, request, queryset):
        if self.value() == Notes.Status.PRIVATE:
            return queryset.filter(is_published=Notes.Status.PRIVATE)
        elif self.value() == Notes.Status.PUBLISHED:
            return queryset.filter(is_published=Notes.Status.PUBLISHED)
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'foot_note','cat','tags']
    filter_horizontal = ['tags']
    prepopulated_fields = {"slug": ("title",)}


    list_display = ('title', 'time_create',
                    'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_private']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [IsPublishedFilter,  'cat__name']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Notes.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_private(self, request, queryset):
        count = queryset.update(is_published=Notes.Status.PRIVATE)
        self.message_user(request, f"{count} записи(ей)сняты с публикации!")

    @admin.display(description="Краткое описание")
    def brief_info(self, note: Notes):
        return f"Содержит {len(note.content)} символов."

    @admin.display(description="Прошло времени после публикации последней заметки")
    def brief_info(self, note: Notes):
        return f"{note.get_next_by_time_create().time_create - note.time_create}"





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# Register your models here.
admin.site.register(TagPost)
admin.site.register(FootNote)
