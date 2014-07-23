from django import forms

class ArticleForm(forms.Form):
    caption = forms.CharField(label='title', max_length=100)
    content = forms.CharField(widget=forms.Textarea)

class TagForm(forms.Form):
    tag_name = forms.CharField()

class ClassificationForm(forms.Form):
    classification_name = forms.CharField()