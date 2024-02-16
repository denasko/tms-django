from django import forms
from django.utils import timezone


class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=100)
    publication_date = forms.DateTimeField(initial=timezone.now().date(),
                                           widget=forms.SelectDateWidget())
    choices = forms.CharField(label='Choices', widget=forms.Textarea)


# class FeedbackForm(forms.Form):
#   feedback_text = forms.CharField(label='Inter your feedback', widget=forms.Textarea)

class FeedbackForm(forms.Form):
    feedback_text = forms.CharField(
        label='Share your thoughts about our site:',
        widget=forms.Textarea(attrs={'placeholder': 'We value your feedback!'}),
        required=False,
        max_length=500,
        help_text='Your feedback is important to us. Maximum 500 characters.'
    )
