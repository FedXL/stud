from django import forms





class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    contend = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':10}))

