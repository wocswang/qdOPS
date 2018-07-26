# -*- coding: utf-8 -*-
# Binder Forms

# 3rd Party
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core import validators
from django.forms import ValidationError
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *
from django.core.exceptions import NON_FIELD_ERRORS

# App Imports
from models import *

class CustomUnicodeListField(forms.CharField):

    def clean(self, value):
        try:
            string_list = [str(cur_rr) for cur_rr in eval(value)]

        except:
            raise ValidationError("Error in converting Unicode list to list "
                                  "of strings: %r" % value)
        return string_list



class FormAddRecord(forms.Form):

    #dns_server = forms.ModelChoiceField(queryset=BindServer.objects.all(),required=True)
    record_name=forms.CharField(max_length=100)
    record_type = forms.ChoiceField(choices=settings.RECORD_TYPE_CHOICES)
    #zone_name = forms.CharField(max_length=100)
    record_data = forms.CharField(max_length=100)
    ttl = forms.ChoiceField(choices=settings.TTL_CHOICES)
    #field_order = ['bindzone']

    def clean(self):
        cleaned_data =super(FormAddRecord,self).clean()
        #dns_server =cleaned_data.get("dns_server")
        record_name=cleaned_data.get("record_name")
        record_type=cleaned_data.get("record_type")
        ttl=cleaned_data.get("ttl")
        record_data=cleaned_data.get("record_data")
        #bindzone = cleaned_data.get("bindzone")

        # if record_name != '':
        #     instnce_exists = BindRecord.objects.filter(bindzone=bindzone,name=record_name).exists()
        #
        #     if instnce_exists:
        #         raise forms.ValidationError('MyModel with this name and parent already exists.')





class FormDeleteRecord(forms.Form):
    dns_server = forms.CharField(max_length=100)
    rr_list = CustomUnicodeListField()








