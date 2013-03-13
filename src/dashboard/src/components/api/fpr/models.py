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

import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
from tastypie.resources import ModelResource
from main import models
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class FPRFileIDResource(ModelResource):
    class Meta:
        queryset = models.FPRFileID.objects.all()
        resource_name = 'FPRFileIDs'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }

class FPRFileIDsBySingleIDResource(ModelResource):
    class Meta:
        queryset = models.FPRFileIDsBySingleID.objects.all()
        resource_name = 'FPRFileIDsBySingleID'
        ordering = ['lastmodified']
        filtering = {
            "pk": ALL,
            "lastmodified": ALL
        }


class FPRCommandsResource(ModelResource):
    class Meta:
        queryset = models.FPRCommands.objects.all()
        resource_name = 'FPRCommands'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }



class FPRCommandRelationshipsResource(ModelResource):
    class Meta:
        queryset = models.FPRCommandRelationships.objects.all()
        resource_name = 'FPRCommandRelationships'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }

class FPRCommandTypesResource(ModelResource):
    class Meta:
        queryset = models.FPRCommandTypes.objects.all()
        resource_name = 'FPRCommandTypes'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRCommandClassificationsResource(ModelResource):
    class Meta:
        queryset = models.FPRCommandClassifications.objects.all()
        resource_name = 'FPRCommandClassifications'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRCommandsSupportedByResource(ModelResource):
    class Meta:
        queryset = models.FPRCommandsSupportedBy.objects.all()
        resource_name = 'FPRCommandsSupportedBy'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRFileIDTypesResource(ModelResource):
    class Meta:
        queryset = models.FPRFileIDTypes.objects.all()
        resource_name = 'FPRFileIDTypes'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRGroupsResource(ModelResource):
    class Meta:
        queryset = models.FPRGroups.objects.all()
        resource_name = 'FPRGroups'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRFileIDGroupMembersResource(ModelResource):
    class Meta:
        queryset = models.FPRFileIDGroupMembers.objects.all()
        resource_name = 'FPRFileIDGroupMembers'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRSubGroupsResource(ModelResource):
    class Meta:
        queryset = models.FPRSubGroups.objects.all()
        resource_name = 'FPRSubGroups'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }
class FPRDefaultCommandsForClassificationsResource(ModelResource):
    class Meta:
        queryset = models.FPRDefaultCommandsForClassifications.objects.all()
        resource_name = 'FPRDefaultCommandsForClassifications'
        ordering = ['lastmodified']
        filtering = {
            "uuid": ALL,
            "lastmodified": ALL
        }


