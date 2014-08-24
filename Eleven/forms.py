from django import forms

class PictureForm(forms.Form):
    imagefile = forms.ImageField()