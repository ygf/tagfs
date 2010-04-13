# -*- coding: utf-8 -*-

# Create your forms here.

from django import forms

class UploadForm(forms.ModelForm):
    """
    Form para subir los ficheros.
    """
    name            = forms.CharField(label='Nombre', max_length=50)
    description     = forms.CharField(label='Descripción', widget=forms.Textarea, max_length=500)
    tags            = forms.CharField(label='Tags', max_length=50)
    data            = forms.FileField(label='Archivo', widget=forms.FileInput)
    replication     = forms.IntegerField(widget=forms.HiddenInput)    
    
    def __unicode__(self):
        return self.name