from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomerProfile, ArtisanProfile, WithdrawalRequest

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
        user.is_artisan = False
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
        user.is_artisan = True
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


class WithdrawalRequestForm(forms.ModelForm):
    """Form for artisans to request withdrawals"""
    
    class Meta:
        model = WithdrawalRequest
        fields = ['amount_requested', 'payment_method', 'bank_account_name', 'bank_account_number', 'mobile_number']
        widgets = {
            'amount_requested': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount (minimum $10)',
                'min': '10',
                'step': '0.01',
                'required': True
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'bank_account_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
            }),
            'bank_account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Account number',
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your mobile number',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount_requested')
        payment_method = cleaned_data.get('payment_method')
        
        # Validate minimum amount
        if amount and amount < 10:
            raise forms.ValidationError('Minimum withdrawal amount is $10.')
        
        # Validate payment method requirements
        if payment_method == 'bank_transfer':
            if not cleaned_data.get('bank_account_name') or not cleaned_data.get('bank_account_number'):
                raise forms.ValidationError('Bank account name and number are required for bank transfer.')
        
        elif payment_method in ['mtn', 'orange']:
            if not cleaned_data.get('mobile_number'):
                raise forms.ValidationError('Mobile number is required for mobile money.')
        
        return cleaned_data