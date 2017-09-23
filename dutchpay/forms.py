from django import forms
import datetime
from .models import Person

class PersonForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = ('name', 'nickname', 'note')

class MeetingForm(forms.Form):
  name = forms.CharField(required=True)
  date = forms.DateField(required=True, initial=datetime.datetime.now(),
                         widget=forms.DateInput(attrs={'class': 'datepicker'}))
  people = forms.ModelChoiceField(required=False, queryset=Person.objects)
