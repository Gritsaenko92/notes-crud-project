from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'reminder_at', 'category']
        widgets = {
            # type='datetime-local' згенерує зручний календар з вибором часу в браузері
            'reminder_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }