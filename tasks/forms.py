#creo este archivo para hacer mis propios formularios
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a descripption'}),
            'important' : forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }