from django import template

register = template.Library()

BAD_WORDS = ['редиска', 'слово', 'пупу','Редиска','Пупу']

# @register.filter(name='censor')
# def censor(value):
#     for word in BAD_WORDS:
#         value = value.replace(word, '*' * len(word))
#     return value

@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in BAD_WORDS:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

