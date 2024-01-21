from django import forms
from .models import Book, Document


class BookForm(forms.ModelForm):
    widgets = {
        'publishDate': forms.TextInput(attrs={'type': 'date'})
    }
    publish_Date = forms.DateField(widget=widgets['publishDate'])

    class Meta:
        model = Book
        fields = '__all__'
        # fields = ['title', 'author']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'document']
