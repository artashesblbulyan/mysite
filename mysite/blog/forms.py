from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from blog import models
from blog.models import Article



class ArticleForm(forms.Form):
    heading = forms.CharField(max_length=70)
    text = forms.CharField(max_length=1000)

    def clean_heading(self):
        _heading = self.cleaned_data["heading"]



        if len(Article.objects.filter(heading=_heading)) == 1:
            raise ValidationError("there is already article with this name")

        return _heading


class ArticleModelForm(forms.ModelForm):
    def clean_heading(self):
        _heading = self.cleaned_data["heading"]


        if len(Article.objects.filter(heading=_heading)) == 1:
            raise ValidationError("there is already article with this heading")

        return _heading

    class Meta:
        model = Article
        fields = "__all__"
