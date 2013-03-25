# This file is part of Archivematica.
#
# Copyright 2010-2013 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.widgets import TextInput, Textarea, RadioSelect
from main import models
from django.conf import settings

class AdministrationForm(forms.Form):
    arguments = forms.CharField(required=False, widget=Textarea(attrs=settings.TEXTAREA_ATTRS))

class AgentForm(ModelForm):
    identifiervalue = forms.CharField(required=True, widget=TextInput(attrs=settings.INPUT_ATTRS))
    name = forms.CharField(required=True, widget=TextInput(attrs=settings.INPUT_ATTRS))

    class Meta:
        model = models.Agent
        exclude = ('identifiertype')

EAD_SHOW_CHOICES = [['embed', 'embed'], ['new','new'], ['none','none'], ['other','other'], ['replace', 'replace']]
EAD_ACTUATE_CHOICES = [['none', 'none'], ['onLoad','onLoad'],['other','other'], ['onRequest', 'onRequest']]
PREMIS_CHOICES = [[ 'yes', 'yes'], ['no', 'no'], ['premis', 'base on PREMIS']]

class ATkForm(forms.Form):
    premis = forms.ChoiceField(widget=RadioSelect(), label="Restrictions Apply:", choices=PREMIS_CHOICES)
    actuate = forms.ChoiceField(widget=RadioSelect(), label="EAD Actuate:", choices=EAD_ACTUATE_CHOICES)
    show = forms.ChoiceField(widget=RadioSelect(), label="EAD Show:", choices=EAD_SHOW_CHOICES)
    usestatement = forms.CharField(widget=TextInput(attrs=settings.INPUT_ATTRS), label="Use statement:")
    objecttype = forms.CharField(widget=TextInput(attrs=settings.INPUT_ATTRS), label="Object type:")
    accessconditions = forms.CharField(widget=TextInput(attrs=settings.INPUT_ATTRS), label="Conditions governing access:")
    useconditions = forms.CharField(widget=TextInput(attrs=settings.INPUT_ATTRS), label="Conditions governing use:")
    urlprefix = forms.CharField(widget=TextInput(attrs=settings.INPUT_ATTRS), label="URL prefix:")
   
     