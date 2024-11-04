from django import forms
from .models import Jobs

class JobPosts(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['post','company_name','description','rating']
