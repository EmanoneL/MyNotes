from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, FootNote, Notes
from django.core.validators import MinLengthValidator, MaxLengthValidator

@deconstructible

class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        #fields = '__all__'
        fields = ['title', 'picture','content', 'is_published', 'cat', 'foot_note', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class':
                                                'form-input'}),
            'content': forms.Textarea(attrs={'cols':
                                                 60, 'rows': 10}),
        }
        labels={'title':'Заголовок'}


    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- ?!.,"

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы и знаки препинания")
        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")