from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "maxlength": "100",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Subject",
                "maxlength": "200",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Write your message here",
                "rows": 6,
            }),
        }

    def clean_website(self):
        website = self.cleaned_data.get("website", "")
        if website:
            raise forms.ValidationError("Invalid submission.")
        return website