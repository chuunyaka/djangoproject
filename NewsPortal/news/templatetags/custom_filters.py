from django import template

register = template.Library()

BAD_WORDS = ['редиска', 'слово', 'пупу','Редиска','Пупу']

@register.filter(name='censor')
def censor(value):
    for word in BAD_WORDS:
        value = value.replace(word, '*' * len(word))
    return value
