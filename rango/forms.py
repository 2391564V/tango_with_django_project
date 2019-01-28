from django import forms
from rango.models import Page, Category

max_length = 128
max_url_length = 200

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=max_length,
        help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Make association between Category and ModelForm
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    name = forms.CharField(max_length=max_length,
        help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=max_url_length,
        help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Make association between Page and ModelForm
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # Check if url exists and if it doesnt begin with http://
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
