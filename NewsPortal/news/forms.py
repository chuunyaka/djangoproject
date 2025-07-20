from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError
from .models import Post, Author, Category
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.mail import send_mail


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'text']

#     def save(self, request):
#         user = super().save(request)
#         common_group = Group.objects.get(name='common')
#         common_group.user_set.add(user)
#         return user


class CommonSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username')

    def save(self, request):
        user = super().save(request)

        # Добавляем в группу
        try:
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)
        except Group.DoesNotExist:
            print("[DEBUG] Группа 'common' не найдена!")

        # Убедимся, что у пользователя есть запись EmailAddress, которая нужна для верификации
        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            verified=False,
            primary=True
        )

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message='Спасибо за регистрацию! Теперь вы можете подписываться на категории и получать уведомления о новостях.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        print(f"[DEBUG] Отправлено приветственное письмо для {user.email}")
        # print(f"[DEBUG] Новый пользователь: {user.username}")
        return user

# class CommonSignupForm(SignupForm):
#     username = forms.CharField(max_length=30, label='Username')
#     def save(self, request):
#         # Вызов базового метода сохранения, который уже создаёт пользователя и проставляет email и пароль
#         user = super().save(request)
#
#     def save(self, request):
#         user = super().save(request)
#         common_group = Group.objects.get(name='common')
#         common_group.user_set.add(user)
#         print(f"[DEBUG] Новый пользователь: {user.username}")
#         print(f"[DEBUG] Подписан на категории: {[c.name for c in Category.objects.filter(subscribers=user)]}")
#         return user
# class CommonSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         print(f"CommonSignupForm: created user {user}")
#         common_group = Group.objects.get(name='common')
#         common_group.user_set.add(user)
#         return user

#     def save(self, request):
#         user = super(CommonSignupForm, self).save(request)
#         common_group = Group.objects.get(name='common')
#         common_group.user_set.add(user)
#         return user