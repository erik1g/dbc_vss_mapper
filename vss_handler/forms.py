from django import forms

class VSSUploadForm(forms.Form):
    file = forms.FileField()
