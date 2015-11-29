from django import forms

class SubmissionDocument(forms.Form):
    docfile = forms.FileField(
        label='Выберите файл',
        help_text='max. 64 килобайт'
    )
