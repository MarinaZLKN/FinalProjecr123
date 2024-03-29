from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .models import Post, Category
from .forms import PostForm, SubscriberForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging
from django.utils import timezone
from datetime import datetime
import pytz  # импортируем стандартный модуль для работы с часовыми поясами
from django.core.paginator import Paginator

logger = logging.getLogger('django')
logger2 = logging.getLogger('django')
logger3 = logging.getLogger('django')



class PostList(ListView):
    logger2.info('checking the page')
    model = Post
    ordering = '-datecreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6


    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = 'posts'
        return context

    def get(self, request):
        current_time = timezone.now()
        posts = Post.objects.get_queryset().order_by('datecreation')
        paginator = Paginator(posts, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'posts': posts,
            'current_time': current_time,
            'page_obj': page_obj,
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'posts.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')



class PostDetail(DetailView):
    logger3.info('checking the post detail')
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        # Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


'''
    @permission_reguired()
    def create_post(reguest):
    form = PostForm()

    if reguest.method == 'POST':
        form = PostForm(reguest.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/posts/')

    return render(reguest, 'create_post.html', {'form': form})'''


class PostSearch(PostList):
    logger.info('Seaching was used')
    model = Post
    ordering = '-datecreation'
    template_name = 'post_search.html'
    context_object_name = 'posts_search'
    paginate_by = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {**super().get_context_data(*args, **kwargs), 'filter': self.get_filter()}


class PostCreate(PermissionRequiredMixin, CreateView):
    logger2.info('checking the create page')
    permission_required = ('NewsPortal.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'



class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class CategoryList(CreateView):
    form_class = SubscriberForm
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('name')

    def post(self, request, *args, **kwargs): #функция подписки на категорию и связи юзера с категорией
        form = SubscriberForm(request.POST)
        if form.is_valid():
            category_subscribers = form.save(commit=False)
            category_subscribers.user = request.user
            category_subscribers.save()
            return HttpResponseRedirect(reverse_lazy('categories'))
        return render(request, 'categories.html', {'form': form})


@login_required
def add_subscribe(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if not is_subscribed:
        cat.subscribers.add(user)
    return redirect('/')
