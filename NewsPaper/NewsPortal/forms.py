from django.core.exceptions import ValidationError
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=30) #упрощаем код, делая быструю проверку на длину статьи


    class Meta:
        model = Post
        fields = [
           'title',
           'text',
           'category_type',
           'author',
           'postCategory',
        ]

    def clean(self):
       cleaned_data = super().clean()  #переопределяем метод clean, чтобы сделать свою проверку
       title = cleaned_data.get("title")    #вытаскиваем то, что будет проверять и кладем в переменную
       text = cleaned_data.get("text")
       if title == text:    #делаем проверку
           raise ValidationError(
               "Описание не должно быть идентично названию."
           )

       return cleaned_data  #возвращаем переменную куда все переопределили
