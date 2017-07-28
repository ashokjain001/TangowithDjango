from django import forms
from django.forms import ModelForm
from models import Category, Page

from django.contrib.auth.models import User
from models import UserProfile

class CategoryForm(ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name of the category")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = "__all__"

class PageForm(ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page ")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        fields = ['category','title','url']
        #fields = ['title']

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
    #fields = ('title','url','views')

class UserForm(ModelForm):
    username = forms.CharField(help_text="Please enter a username: ")
    email = forms.CharField(help_text="Please enter your email: ")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter your Password: ")

    class Meta:
        model = User
        fields = ['username','email','password']

class UserProfileForm(ModelForm):
    website = forms.URLField(help_text="Please enter your website: ", required = False)
    picture = forms.ImageField(help_text="Select a profile image to upload: ", required=False)

    class Meta:
        model = UserProfile
        fields = ['website','picture']