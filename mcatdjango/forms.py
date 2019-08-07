'''
MCAT Meeting Coordination Assistance Tool for Django
'''
__author__ = "Takayuki Kannon <kannon@brain.riken.jp>"

from django import forms


class PostLoginForm(forms.Form):
    first_name = forms.CharField(max_length=30,required=False)
    last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(required=True)