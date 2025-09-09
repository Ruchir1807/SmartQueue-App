from django import forms
from .models import Service

class JoinQueueForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Select Service")

class CheckStatusForm(forms.Form):
    token_number = forms.CharField(label="Enter your Token Number")
