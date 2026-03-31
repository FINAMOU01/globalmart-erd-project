from django import forms
from django.contrib.auth import get_user_model
from .models import Product, Category, ArtisanRating

User = get_user_model()


class ProductForm(forms.ModelForm):
    """
    Form for artisans to create and edit their products.
    Automatically sets the artisan to the current logged-in user.
    """
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'currency_code', 'stock_quantity', 'image', 'attributes', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Product Description',
                'rows': 5,
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'step': '0.01',
                'min': '0',
                'required': True,
            }),
            'currency_code': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock Quantity',
                'min': '0',
                'required': True,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'attributes': forms.HiddenInput(),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attributes'].required = False
        self.fields['is_featured'].required = False
        
        # Enhance currency choices with country flags (for form display)
        flag_choices = [
            ('USD', 'USD - US Dollar'),
            ('EUR', 'EUR - Euro'),
            ('GBP', 'GBP - British Pound'),
            ('XAF', 'XAF - CFA Franc (Central)'),
            ('NGN', 'NGN - Nigerian Naira'),
            ('GHS', 'GHS - Ghanaian Cedi'),
            ('KES', 'KES - Kenyan Shilling'),
            ('ZAR', 'ZAR - South African Rand'),
            ('EGP', 'EGP - Egyptian Pound'),
            ('MAD', 'MAD - Moroccan Dirham'),
        ]
        self.fields['currency_code'].choices = flag_choices
        
        # Make image optional when editing (if instance exists)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
            self.fields['image'].widget.attrs['required'] = False
    
    def clean_attributes(self):
        """
        Validate that attributes is valid JSON if provided.
        """
        import json
        attributes = self.cleaned_data.get('attributes')
        
        if attributes:
            if isinstance(attributes, str):
                try:
                    json.loads(attributes)
                except json.JSONDecodeError:
                    raise forms.ValidationError("Attributes must be valid JSON format.")
        
        return attributes


class ArtisanProfileForm(forms.Form):
    """
    Form for artisans to update their profile information.
    """
    
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number',
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Country',
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['phone'].initial = self.user.phone
            self.fields['country'].initial = self.user.country
    
    def save(self, commit=True):
        """
        Save user data.
        """
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            self.user.phone = self.cleaned_data.get('phone', '')
            self.user.country = self.cleaned_data.get('country', '')
            
            if commit:
                self.user.save()
        
        return self.user


class ArtisanBioForm(forms.Form):
    """
    Form for artisan profile bio and social links.
    """
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell your story...',
            'rows': 5,
        })
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
        })
    )
    social_links = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '{"instagram":"url","facebook":"url","twitter":"url"}',
            'rows': 3,
        })
    )
    
    def clean_social_links(self):
        """
        Validate that social_links is valid JSON if provided.
        """
        import json
        social_links = self.cleaned_data.get('social_links')
        
        if social_links:
            if isinstance(social_links, str):
                try:
                    json.loads(social_links)
                except json.JSONDecodeError:
                    raise forms.ValidationError("Social links must be valid JSON format.")
        
        return social_links


class ArtisanRatingForm(forms.ModelForm):
    """
    Form for rating artisans
    """
    class Meta:
        model = ArtisanRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with this artisan (optional)',
                'rows': 4,
            }),
        }
