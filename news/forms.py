from django import forms

from news.models import Comment


class CommentForm(forms.ModelForm):
    """Форма комментов"""

    class Meta:
        model = Comment
        fields = ("text",)
