from django import forms

class UploadForm(forms.Form):
    minutes = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )