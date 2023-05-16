from django import forms

from django.contrib.auth.forms import UserCreationForm

from myblog.models import Comment, Post, UserProfileInfo


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = UserProfileInfo
        fields = ('username', 'email', 'confirm_password')



class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'text', 'picture')
        widgets = {
            
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)

    widgets = {
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
    }

