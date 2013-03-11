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

from django.conf.urls.defaults import *
from components.api.fpr.models import FPRFileIDResource
from components.api.fpr.models import FPRFileIDsBySingleIDResource
from components.api.fpr.models import FPRCommandsResource
from components.api.fpr.models import FPRCommandRelationshipsResource
from components.api.fpr.models import FPRCommandTypesResource
from components.api.fpr.models import FPRCommandClassificationsResource
from components.api.fpr.models import FPRCommandsSupportedByResource
from components.api.fpr.models import FPRFileIDTypesResource
from components.api.fpr.models import FPRGroupsResource
from components.api.fpr.models import FPRFileIDGroupMembersResource
from components.api.fpr.models import FPRSubGroupsResource
from components.api.fpr.models import FPRDefaultCommandsForClassificationsResource

from tastypie.api import Api

# add version to FPR resources
api = Api(api_name='v1')
api.register(FPRFileIDResource())
api.register(FPRFileIDsBySingleIDResource())
api.register(FPRCommandsResource())
api.register(FPRCommandRelationshipsResource())
api.register(FPRCommandTypesResource())
api.register(FPRCommandClassificationsResource())
api.register(FPRCommandsSupportedByResource())
api.register(FPRFileIDTypesResource())
api.register(FPRGroupsResource())
api.register(FPRFileIDGroupMembersResource())
api.register(FPRSubGroupsResource())
api.register(FPRDefaultCommandsForClassificationsResource())

urlpatterns = patterns('components.archival_storage.views',
    (r'', include(api.urls)),
)
