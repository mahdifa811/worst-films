from django import forms
from .models import Profile


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
        
    class Meta:
        model = Profile
        fields = (
            "bio",
            "age"
        )
        widgets= {
            'bio': forms.Textarea(attrs= {'class':'form-control'})
        }