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
        fields =('title', 'text', 'image', 'tags')

        # here i pass what are the field required for the form and validate

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class META:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Username
    def clean_username(self):
        username = self.cleaned_data['username']
        if 'admin' in username.lower():
            raise forms.ValidationError("Username cannot contain 'admin")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
# Validate Email
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered")
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail addresses are allowed")
        return email
    
# Validate Password
    def clean(slef):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 character")
        
        return cleaned_data


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.cleaned_data['username']
        if 'admin' in username.lower():
            raise forms.ValidationError("Username cannot contain 'admin")
        return username
    
    password = forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
