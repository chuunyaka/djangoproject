from django.core.exceptions import ValidationError
from .models import Post, Author
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
