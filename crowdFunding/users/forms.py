from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    #birth_date = forms.DateField(required=False,help_text='Optional.')
    phone = forms.CharField(max_length=11,required=False, help_text='Optional.')
    user_image = forms.ImageField(label = "upload your image",required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2','user_image')
        unique_together = ('email',)

class UserUpdateForm(forms.ModelForm):
   

    class Meta:
         model = User
         fields = ['first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
         model = Profile
         fields = ['user_image', 'birth_date', 'country', 'facebook', 'phone']


# class UserFormPassword(ModelForm):
#     class Meta:
#         model = User
#         fields = ['password',]

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []   #Form has only submit button.  Empty "fields" list still necessary, though.
