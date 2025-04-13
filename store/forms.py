# store/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Review, UserProfile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
class SignUpForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')