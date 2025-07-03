from django import forms 

from .models import Post 
from .models import Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# forms.ModelForm is responsible for telling django that this form is a model form
class PostForm(forms.ModelForm): 

# tell django which model should be created from this form
    class Meta:
        model = Post
        fields =('title', 'text', 'image')

        # here i pass what are the field required for the form

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
