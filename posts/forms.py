from django import forms

class ReplyForm(forms.Form):
    reply_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Reply to this comment...'}))
