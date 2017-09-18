from django import forms

from .models import Meeting, Person

class PersonForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = ('name', 'nickname', 'note')
