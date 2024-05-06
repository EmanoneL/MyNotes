from datetime import timezone

from django.contrib.admin import SimpleListFilter
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


# Create your models here.
def unidecode(title):
    pass


class UnPublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Notes.Status.PRIVATE)


class Notes(models.Model):
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    class Status(models.IntegerChoices):
        PRIVATE = 0, 'Личное'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    private = UnPublishedModel()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug':
                                           self.slug})

    def __str__(self):
        return self.title

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x:(bool(x[0]), x[1]), Status.choices)),default=Status.PRIVATE, verbose_name="Статус")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги")
    foot_note = models.OneToOneField('FootNote', on_delete=models.SET_NULL, null=True, blank=True, related_name='note', verbose_name="Примечание")
    picture = models.ImageField(upload_to="pictures/%Y/%m/%d/",
                              default=None, blank=True, null=True,
                              verbose_name="Изображение")


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('categories', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
                                          self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.tag, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag


class FootNote(models.Model):
    class Meta:
        verbose_name = 'Примечание'
        verbose_name_plural = 'Примечания'
    content = models.TextField(blank=True)

    def __str__(self):
        return self.content


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
