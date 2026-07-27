from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from quotes.models import Quote, Author

class AddAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class AddQuote(forms.ModelForm):
    class Meta:
        model = Quote
        exclude = ['added_by']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')