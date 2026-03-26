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
        self.fields['username'].help_text = 'Use letters, numbers, and @/./+/-/_ only'
        self.fields['password1'].help_text = 'Enter a password'
        self.fields['password2'].help_text = 'Confirm your password'
        # Allow any password including similar to username
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

    def clean_password2(self):
        """Override - only check if passwords match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.', code='password_mismatch')
        return password2

    def _post_clean(self):
        """Override to allow passwords similar to username"""
        # Suppress the UserCreationForm's password similarity check
        original_add_error = self.add_error
        def filtered_add_error(field, error):
            if field == 'password2' and 'too similar' in str(error).lower():
                return
            return original_add_error(field, error)
        
        self.add_error = filtered_add_error
        try:
            super()._post_clean()
        finally:
            self.add_error = original_add_error

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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
        self.fields['username'].help_text = 'Use letters, numbers, and @/./+/-/_ only'
        self.fields['password1'].help_text = 'Enter a password'
        self.fields['password2'].help_text = 'Confirm your password'
        # Allow any password including similar to username
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

    def clean_password2(self):
        """Override - only check if passwords match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.', code='password_mismatch')
        return password2

    def _post_clean(self):
        """Override to allow passwords similar to username"""
        # Suppress the UserCreationForm's password similarity check
        original_add_error = self.add_error
        def filtered_add_error(field, error):
            if field == 'password2' and 'too similar' in str(error).lower():
                return
            return original_add_error(field, error)
        
        self.add_error = filtered_add_error
        try:
            super()._post_clean()
        finally:
            self.add_error = original_add_error

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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