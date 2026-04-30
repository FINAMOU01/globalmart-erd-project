from django import forms
from django.contrib.auth import get_user_model
from .models import Product, Category, ArtisanRating
from accounts.models import ArtisanProfile

User = get_user_model()


class ProductForm(forms.ModelForm):
    """
    Form for artisans to create and edit their products.
    Automatically sets the artisan to the current logged-in user.
    Images are managed separately through the ProductImage model.
    """
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'currency_code', 'stock_quantity', 'sku', 'reorder_level', 'is_featured']
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
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU (optional)',
            }),
            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Reorder Level',
                'min': '0',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_featured'].required = False
        self.fields['sku'].required = False
        
        # Enhance currency choices
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


class ArtisanBioForm(forms.ModelForm):
    """
    ModelForm for artisan profile bio, picture and social links.
    Properly handles file uploads and saves to ArtisanProfile model.
    """
    
    social_links = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '{"instagram":"url","facebook":"url","twitter":"url"}',
            'rows': 3,
        })
    )
    
    class Meta:
        model = ArtisanProfile
        fields = ['bio', 'profile_picture', 'social_links']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell your story...',
                'rows': 5,
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make profile_picture optional when editing
        self.fields['profile_picture'].required = False
        # Convert JSON dict to string for form display
        if self.instance and self.instance.social_links:
            import json
            self.fields['social_links'].initial = json.dumps(self.instance.social_links)
    
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
    
    def save(self, commit=True):
        """
        Save the artisan profile with proper JSON handling for social_links.
        """
        instance = super().save(commit=False)
        
        # Handle social_links JSON
        if self.cleaned_data.get('social_links'):
            import json
            try:
                instance.social_links = json.loads(self.cleaned_data.get('social_links'))
            except:
                pass
        
        if commit:
            instance.save()
        return instance


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
