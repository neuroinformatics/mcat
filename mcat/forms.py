'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django import forms
from django.utils.translation import ugettext_lazy as _

from mcat import settings
from mcat.models import Meeting, Attend

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('user', 'code', 'view_key', 'date_available')
        widgets = {
            'title'       : forms.TextInput(attrs={'class':"form-control", 'placeholder':_("Board of directors' meeting")}),
            'place'       : forms.TextInput(attrs={'class':"form-control", 'placeholder':_("Seminar room")}),
            'date_start'  : forms.DateInput(attrs={'class':"form-control datepicker"}),
            'date_end'    : forms.DateInput(attrs={'class':"form-control datepicker"}),
            'time_slot'   : forms.RadioSelect(),
            'time_start'  : forms.Select(attrs={'class':"form-control"}),
            'time_end'    : forms.Select(attrs={'class':"form-control"}),
            'option_mode' : forms.RadioSelect(),
            'remarks'     : forms.Textarea(attrs={'rows': 5, 'class': "form-control"}),
        }

class MeetingDetailForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ('user', 'code', 'view_key')
        widgets = {
            'title'          : forms.HiddenInput(),
            'place'          : forms.HiddenInput(),
            'date_start'     : forms.HiddenInput(),
            'date_end'       : forms.HiddenInput(),
            'time_slot'      : forms.HiddenInput(),
            'time_start'     : forms.HiddenInput(),
            'time_end'       : forms.HiddenInput(),
            'option_mode'    : forms.HiddenInput(),
            'remarks'        : forms.HiddenInput(),
            'date_available' : forms.HiddenInput(),
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Attend
        exclude = ('code', 'update_key')
        widgets = {
            'name'        : forms.TextInput(attrs={'class':"form-control"}),
            'mail'        : forms.TextInput(attrs={'class':"form-control", 'placeholder':"mail@example.com"}),
            'comment'     : forms.Textarea(attrs={'rows': 5, 'class': "form-control"}),
            'date_attend' : forms.HiddenInput(),
        }

class DeleteForm(forms.Form):
    code = forms.CharField(max_length=settings.code_length, label=_("Meeting Code"), widget=forms.HiddenInput())
    view_key = forms.CharField(max_length=settings.code_length, label=_("View Key"), widget=forms.HiddenInput())
