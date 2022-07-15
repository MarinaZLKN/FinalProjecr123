from django_filters import *
from .models import Post, Author, Category, CategorySubscribers
from django.forms.widgets import DateInput


class PostFilter(FilterSet):
    date = DateFilter(field_name='datecreation',
                      lookup_expr='lte',
                      label='Создано до',
                      widget=DateInput(attrs={'type': 'date'}))
    title = CharFilter(lookup_expr='icontains')
    postCategory = ModelChoiceFilter(queryset=Category.objects.all())
    author = ModelChoiceFilter(queryset=Author.objects.all())
    date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY. Example: 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}

    class Meta:
        model = Post
        fields = ['date', 'title', 'author', 'postCategory', 'category_type']


class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())
    user = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = CategorySubscribers
        fields = ['category']
