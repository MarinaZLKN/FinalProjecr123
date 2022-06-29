from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect

class PostList(ListView):
    model = Post
    ordering = '-datecreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {**super().get_context_data(*args, **kwargs), 'filter': self.get_filter(), 'news' : 'posts,'}


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


def create_post(reguest):
    form = PostForm()

    if reguest.method == 'POST':
        form = PostForm(reguest.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/posts/')

    return render(reguest, 'create_post.html', {'form': form})

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
