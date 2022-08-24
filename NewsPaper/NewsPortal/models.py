from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


#Сначала создаю проект и в нем приложение, которое обязательно записываю в settings.py
#Затем в этом файле сразу прописываю каркасы таблиц - сначала создаю классы и методы и потом начинаю описывать их


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)   #связь пользователя с автором через встроенную
    # модель User, которую не забываем импортировать
    ratingAuthor = models.SmallIntegerField(default=0)  #рейтинг автора - начинаем с 0

    def __str__(self):
        return f'{self.authorUser}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))     #к модели post променяем ф-ю aggregate, которая
        # применяет  ф-ю sum к полю rating  и он складывает все значения поля rating у модели post связанных с
        # этим автором
        pRat = 0 #изначальный рейтинг равен 0
        pRat += postRat.get('postRating') #postRating это мы дали имя всем значениям рейтинга и в этой строчке суммировали его

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))     #тоже самое для рейтинга
        # комментов, но связываем уже с пользователем
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = pRat * 3 + cRat     # складываем
        self.save() #сохраняем


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True) #название категории не будет длинным словом,поэтому ставим
    # макс 64 символа, но обязательный аргемент унивальность. чтобы категории не повторялись
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    #публикация имеет связь один к многим, поскольку
    # один автор может написать множесто статей
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)   #поле категории
    # определяем из списка категорий выше, по умолчанию статья.
    datecreation = models.DateTimeField(auto_now_add=True)  #выбираем свойство сохранения автоматического время создания
    postCategory = models.ManyToManyField(Category, through='PostCategory')     #связь многие к многим, поскольку
    # публикации могут быть разных категорий и наоборот
    title = models.CharField(max_length=128)    #ставим среднее колисетво символов для названия
    text = models.TextField()   #неограниченное количсество символов для самой новости или статьи
    rating = models.SmallIntegerField(default=0)    #рейтинг статьи по умолчанию 0

    def like(self):
        self.rating += 1    #прибавляем к рейтингу единицу
        self.save()     #и сохраняем изменения

    def dislike(self):
        self.rating -= 1  #отнимаем от рейтинга единицу
        self.save()

    def preview(self):
        return self.text[0:123] + '...'     #по сути отображение первых символов статьи и последующее многоточие

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post_detail-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):   #промежуточная модель
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)     #публикации
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)     #категории

    def __str__(self):
        return f'{self.categoryThrough}'


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)     #какой модели мы присаиваем комментарий
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)     #связь комментарий-пользователь, чтобы каждый
    # пользователь мог оставлять разным статьям комментарии
    text = models.TextField()   #текст для комментария
    datecreation = models.DateTimeField(auto_now_add=True)  #автоматич время создания
    rating = models.SmallIntegerField(default=0)    #рейтинг комментария

    def like(self):
        self.rating += 1  # прибавляем к рейтингу единицу
        self.save()  # и сохраняем изменения

    def dislike(self):
        self.rating -= 1  # отнимаем от рейтинга единицу
        self.save()

    def __str__(self):
        return f'{self.text}'


class CategorySubscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.category}'
