from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Виберіть файл (CSV або Excel)',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv, .xls, .xlsx'})
    )
