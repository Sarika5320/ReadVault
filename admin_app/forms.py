from django import forms
from user_app.models import Book,Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)