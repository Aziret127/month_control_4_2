from django import forms
from CineBoard.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import Movie


GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo_number = forms.CharField(max_length=15, initial='+996', required=True)
    gender = forms.ChoiceField(choices=GENDER,  required=True)
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'photo_number',
            'gender',
            'city'
        )
    
    def save(self, commit = True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'