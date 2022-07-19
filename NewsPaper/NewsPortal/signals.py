from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, mail_managers
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from .models import Post


domain = Site.objects.get_current().domain
obj = Post.objects.filter(pk=id)
path = obj.get_absolute_url()
url = 'http://{domain}{path}'.format(domain=domain, path=path)

@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postCategory.all():
            for subscribe in CategorySubscribers.objects.filter(category=cat):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.text,
                    from_email='MarinaRAhven@yandex.ru',
                    to=[subscribe.user.email],
                )



                html_content = render_to_string(
                    'post_created.html',
                    {
                        'post': instance,
                        'recipient': subscribe.user.email,

                    }
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()


                print(f'{instance.title} {instance.text}')
                print('Уведомление отослано подписчику ', subscribe.user, 'на почту', subscribe.user.email, ' на тему ', subscribe.category)