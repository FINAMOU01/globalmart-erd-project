from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomerProfile, ArtisanProfile

User = get_user_model()


class CustomerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add helpful text to username field
        self.fields['username'].help_text = 'Use letters, numbers, and @/./+/-/_ only (no spaces or special characters)'
        # Remove password validators - allow any password
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        # Add help text for password fields
        self.fields['password1'].help_text = 'Enter a password'
        self.fields['password2'].help_text = 'Confirm your password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'customer'
        if commit:
            user.save()
        return user


class ArtisanRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add helpful text to username field
        self.fields['username'].help_text = 'Use letters, numbers, and @/./+/-/_ only (no spaces or special characters)'
        # Remove password validators - allow any password
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        # Add help text for password fields
        self.fields['password1'].help_text = 'Enter a password'
        self.fields['password2'].help_text = 'Confirm your password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'artisan'
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))


class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'profile_picture']


class ArtisanProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ArtisanProfile
        fields = ['phone', 'address', 'profile_picture']