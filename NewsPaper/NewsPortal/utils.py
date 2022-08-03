from datetime import datetime, timedelta
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post


def send_subscriber_email(subscriber, instance):
    message = EmailMultiAlternatives(
        subject=instance.title,
        body=instance.text,
        from_email='MarinaRAhven@yandex.ru',
        to=[subscriber.user.email],
    )
    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
            'recipient': subscriber.user.email,
            'name': subscriber.user

        }
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

    print(f'{instance.title} {instance.text}')
    print('Уведомление отослано подписчику ', subscriber.user, 'на почту', subscriber.user.email, ' на тему ',
          subscriber.category)


def notify_all_subscribers():
    last_week_date = datetime.now().date() - timedelta(days=7)

    for instance in Post.objects.filter(datecreation__gt=last_week_date):
        for subscriber in CategorySubscribers.objects.filter(category=instance.postCategory):
            send_subscriber_email(subscriber=subscriber, instance=instance)


def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postCategory.all():
            for subscriber in CategorySubscribers.objects.filter(category=cat):
                send_subscriber_email(subscriber=subscriber, instance=instance)
