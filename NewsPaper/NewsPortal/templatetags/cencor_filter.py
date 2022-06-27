from django import template

register = template.Library()

CENSOR_LIST = ['выход', 'спикер', 'список', 'роль', 'продукты']

@register.filter(name='censor')
def censor(value):
    for word in value.split():
        if word.lower() in CENSOR_LIST:
            x = word.replace(word[1:], '*' * (len(word)-1))
            value = value.replace(word, x)
            return value
    return value

