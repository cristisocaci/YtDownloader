from django import forms


class VideoForm(forms.Form):
    title = forms.CharField()
    song = forms.CharField(required=False)
    artist = forms.CharField(required=False)
    album = forms.CharField(required=False)
