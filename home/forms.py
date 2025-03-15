from dataclasses import field, fields
from pyexpat import model
from django import forms
from .models import Author,Book


class AuthorForm(forms.ModelForm):
    
    class Meta:
        model = Author
        fields = ('name',)

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = '__all__'