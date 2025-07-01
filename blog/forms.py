from django import forms 

from .models import Post 

# forms.ModelForm is responsible for telling django that this form is a model form
class PostForm(forms.ModelForm): 

# tell django which model should be created from this form
    class Meta:
        model = Post
        fields =('title', 'text')

        # here i pass what are the field required for the form