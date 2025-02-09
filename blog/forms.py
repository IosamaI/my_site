from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        
        widgets = {
            
            "comment_text": forms.Textarea(attrs={"rows": 3}),  # Add rows for better formatting
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_text'].error_messages = {
            'required': 'Please enter your comment.',
        }