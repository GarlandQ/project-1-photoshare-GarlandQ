from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Comment..."}
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ["content"]

        # widgets = {
        #     "content": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Comment..."}
        #     )
        # }
