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

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PRIVATE)

