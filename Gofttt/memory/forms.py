from django import forms
from .models import Memory,Comment,Report,DelCast
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.contenttypes.models import ContentType
 

 
 
class MemoryForm(forms.ModelForm):
 
    class Meta:
        model = Memory
        fields= ['title','category','body','image', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'موضوع خاطره شما'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'body': CKEditorWidget(),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'audio_file': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
 
 
 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.content_object = kwargs.pop('content_object', None)
        super().__init__(*args, **kwargs)

        if self.content_object:
            content_type = ContentType.objects.get_for_model(self.content_object)
            self.fields['content_type'] = forms.IntegerField(
                initial=content_type.id,
                widget=forms.HiddenInput()
            )
            self.fields['object_id'] = forms.IntegerField(
                initial=self.content_object.id,
                widget=forms.HiddenInput()
            )

    def clean(self):
        cleaned_data = super().clean()
        # اعتبارسنجی امنیتی
        if self.content_object:
            content_type = ContentType.objects.get_for_model(self.content_object)
            if cleaned_data.get('content_type') != content_type.id:
                raise forms.ValidationError("Invalid content type")
            if cleaned_data.get('object_id') != self.content_object.id:
                raise forms.ValidationError("Invalid object ID")
        return cleaned_data

    def save(self, user=None, commit=True):
        comment = super().save(commit=False)
        comment.user = user
        if self.content_object:
            comment.content_type = ContentType.objects.get_for_model(self.content_object)
            comment.object_id = self.content_object.id
        if commit:
            comment.save()
        return comment

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reason for report', 'rows': 4}),
            'user': forms.HiddenInput(),
            'memory': forms.HiddenInput(),
        }

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        if not reason:
            raise forms.ValidationError("Please provide a reason for the report.")
        return reason



class DelCastForm(forms.ModelForm):
    class Meta:
        model = DelCast
        fields = [
            'title',
            'Occasion',
            'Recipients_name_surname',
            'caption',
            'time',
            'image',
            'audio_file'
        ]
        widgets = {
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'Occasion': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
            'audio_file': forms.Select(attrs={'class': 'form-control'})
        }