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

from django.conf import settings

import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
#we are getting lookup values directly from db, not using django models
from django.db import connection, transaction

from django import forms
from django.forms.widgets import *
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from main import models
from components import helpers
from components.preservation_planning import models as ppModels 

INPUT_ATTRS = {'class': 'span11'}

def getTools():
    query = 'SELECT description FROM FileIDTypes'

    cursor = connection.cursor()
    cursor.execute(query)

    ret = []
    for tool in cursor.fetchall():
        ret.append( (tool[0], tool[0]) )

    return ret

def getCommandTypes():
    query = 'SELECT type from CommandTypes'
    
    cursor = connection.cursor()
    cursor.execute(query)
    
    ret = []
    for commandType in cursor.fetchall():
        ret.append( (commandType[0], commandType[0]) )

    return ret

def getCommands(usage = 'command'):
    
    query = 'Select pk, description from Commands where commandUsage = "{}"'.format(usage)
    
    cursor = connection.cursor()
    cursor.execute(query)
    
    ret = []
    ret.append(('','None'))
    for vCommand in cursor.fetchall():
        ret.append( (vCommand[0], vCommand[1]) )
    
    return ret
        
def getPurposes():
    query = 'SELECT classification FROM CommandClassifications'

    cursor = connection.cursor()
    cursor.execute(query)

    ret = []
    for purpose in cursor.fetchall():
        ret.append( (purpose[0], purpose[0]) )

    return ret

def getFormatIDs(purpose = 'all'):
    query = 'Select pk, description from FileIDs';
    if purpose == 'access':
        query = 'Select pk, description from FileIDs where validAccessFormat = 1'
    elif purpose == 'preservation':
        query = 'Select pk, description from FileIDs where validPreservationFormat = 1'
        
    cursor = connection.cursor()
    cursor.execute(query)
    
    ret = []
    ret.append(('', 'None'))
    for formatID in cursor.fetchall():
        ret.append( (formatID[0], formatID[1]))

    return ret

class FPRSearchForm(forms.Form):
    query = forms.CharField(label='', required=False, widget=TextInput(attrs=settings.INPUT_ATTRS))
      
class FPREditFormatID(ModelForm):
    uuid = forms.HiddenInput()
    lastModified = forms.HiddenInput()
    tool = forms.ChoiceField(choices = getTools(), label= "File Identification Tool")
    description = forms.CharField(label = 'Format ID Description', required = False, max_length = 100,
        widget = TextInput(attrs = {'class':'Description'}))
    validpreservationformat = forms.BooleanField(required=False, initial=False, label = 'Valid for Preservation') 
    validaccessformat = forms.BooleanField(required=False, initial=False, label='Valid for Access') 
    replaces = forms.ChoiceField(choices = getFormatIDs())
    enabled = forms.BooleanField(required=False, initial=True) 
    class Meta:
        model = ppModels.FormatID
        exclude = ('lastModified',)

class FPREditCommand(ModelForm):
    COMMAND_USAGE_CHOICES = (('command','command'), ('verification','verification'), ('eventDetail','eventDetail'))
    uuid = forms.HiddenInput()
    lastModified = forms.HiddenInput()
    commandUsage = forms.ChoiceField(choices = COMMAND_USAGE_CHOICES, label='Usage')
    commandType = forms.ChoiceField(choices = getCommandTypes())
    command = forms.CharField(label = 'Command', required = False, max_length = 100,
        widget = TextInput(attrs = {'class':'Description'}))
    outputLocation = forms.CharField(label= 'Output location', required= False, max_length = 255,
        widget =  TextInput(attrs = {'class':'Description'}))
    outputFileFormat = forms.CharField(label= 'Output File Format', required= False, max_length = 15,
        widget =  TextInput(attrs = {'class':'Description'}))
    description = forms.CharField(label = 'Description', required = False, max_length = 100,
        widget = TextInput(attrs = {'class':'Description'}))
    verificationCommand = forms.ChoiceField(choices = getCommands('verification'), label = 'Verification command', required = False)
    eventDetailCommand = forms.ChoiceField(choices = getCommands('eventDetail'), label = 'Event detail command', required = False)
    class Meta:
        model = ppModels.Command
        exclude = ('supportedBy', 'lastModified',)
        
class FPREditRule(ModelForm):
    uuid = forms.HiddenInput()
    lastModified = forms.HiddenInput()
    purpose = forms.ChoiceField(choices = getPurposes())
    formatID = forms.ChoiceField(choices = getFormatIDs(), label = 'Format ID', required = True)
    command = forms.ChoiceField(choices = getCommands(), label = 'Command', required = True)
    replaces = forms.CharField(max_length=50)
    enabled = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = ppModels.FormatPolicyRule  
        exclude = ('lastModified',)
            
class FPREditToolOutput(ModelForm):
    uuid = forms.HiddenInput()
    lastModified = forms.HiddenInput()
    formatID = forms.ChoiceField(choices = getFormatIDs(), label='Format ID', required = True)
    toolOutput = forms.CharField(label = 'Tool output', required=True, max_length=50)
    tool = forms.ChoiceField(choices = getTools())
    toolVersion = forms.CharField(max_length=20, label='Tool version')
    replaces = forms.CharField(max_length=50)
    enabled = forms.BooleanField(required=False, initial=True)
    class Meta:
        model = ppModels.FormatIDToolOutput
        exclude = ('lastModified',)
      
