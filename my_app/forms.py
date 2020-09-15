from django import forms

from .models import Member, Peminjaman, Book


class DateInput(forms.DateInput):
    input_type = 'date'


class MemberForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Member
        fields = [
            'name',
            'address',
            'email',
            'date_born',
            ]
        widgets = {
            'date_born': DateInput(),
        }


class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = (
            'author',
            'title',
            'denda',
            'denda_hilang',
            'rating',
            'categorie',
        )
