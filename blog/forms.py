from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from blog.models import Post

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name','last_name':'Last_Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control md-6'}),
        'first_name':forms.TextInput(attrs={'class':'form-control md-6'}),
        'last_name':forms.TextInput(attrs={'class':'form-control md-6'}),
        'email':forms.EmailInput(attrs={'class':'form-control md-6'})


        
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label='Password',strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        labels = {'title':'Title','author':'Author','desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'author':forms.TextInput(attrs={'class':'form-control'}),
                   'desc':forms.Textarea(attrs={'class':'form-control'}),}


