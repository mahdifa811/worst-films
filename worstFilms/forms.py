from django import forms
from .models import Film, Comment

class FilmForm(forms.ModelForm):
    
    class Meta:
        model = Film
        fields = (
            "title",
            "director",
            "country",
            "poster",
            "release_year",
            "rate",
            "review"
            )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= (
            "body",
        )
        widgets= {
            'body': forms.Textarea(attrs= {'class':'form-control'})
        }
        messages= {
            'body':{
                'required': 'please fill the field essentially!'
            }
        }
        help_texts= {
            'body': 'please comment in this field'
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= (
            "body",
        )

