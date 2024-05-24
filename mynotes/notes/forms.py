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

    # title = forms.CharField(label='Заголовок',
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         validators=[
    #                             MaxLengthValidator(255, message='Максимум 100 символов'),]
    #
    #                         )
    #
    # content = forms.CharField(widget=forms.Textarea(),
    #                           required=False,
    #                           label='Контент',
    #                           validators=[
    #                               MinLengthValidator(5, message='Минимум 5 символов')]
    #                           )
    # is_published = forms.BooleanField(required=False,
    #                                   label='Статус')
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                              label='Категория',
    #                              empty_label="Категория не выбрана" )
    # foot_note = forms.ModelChoiceField(queryset=FootNote.objects.all(),
    #                                    required=False,
    #                                    label='Примечание',
    #                                    empty_label="Без примечания")
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- ?!.,"

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы и знаки препинания")
        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")