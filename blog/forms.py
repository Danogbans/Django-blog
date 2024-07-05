from django import forms
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from taggit.forms import TagWidget
from ckeditor.widgets import CKEditorWidget




class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.template_pack = 'bootstrap4'

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, CKEditorWidget):   # Skip CKEditorWidget
                field.widget.attrs['class'] = 'form-control'




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Comment', css_class='btn btn-primary'))
        self.helper.template_pack = 'bootstrap4'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(EmailPostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Email', css_class='btn btn-primary'))
        self.helper.template_pack = 'bootstrap4'



class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=255)