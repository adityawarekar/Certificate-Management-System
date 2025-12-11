from django import forms

class LookupForm(forms.Form):
    email = forms.EmailField(required=False, label="Email")
    participant_id = forms.CharField(required=False, label="Participant ID")
    full_name = forms.CharField(required=False, label="Full name (optional)")
