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

import os, ConfigParser, simplejson
from django.http import Http404, HttpResponse, HttpResponseForbidden
from tastypie.authentication import ApiKeyAuthentication
from contrib.mcp.client import MCPClient
from main import models

#
# Example: curl --data \
#   "username=mike&api_key=d3b0e878a47ceb4c77b931a55c7007cf8d541d47&directory=MyTransfer" \
#   http://127.0.0.1/api/transfer/approve
#
#
def approve_transfer(request):
    if request.method == 'POST':
        api_auth = ApiKeyAuthentication()
        authorized = api_auth.is_authenticated(request)
        if authorized == True:
            message = ''
            error   = None

            directory = request.POST.get('directory', '')
            error = approve_transfer_via_mcp(directory)

            response = {}

            if error != None:
                response['message'] = error
                response['error']   = True
            else:
                response['message'] = 'Approval successful.'

            return HttpResponse(
                simplejson.JSONEncoder().encode(response),
                mimetype='application/json'
            )
        else:
            return HttpResponseForbidden()
    else:
        raise Http404

def get_server_config_value(field):
    clientConfigFilePath = '/etc/archivematica/MCPServer/serverConfig.conf'
    config = ConfigParser.SafeConfigParser()
    config.read(clientConfigFilePath)

    try:
        return config.get('MCPServer', field) # "watchDirectoryPath")
    except:
        return ''

def approve_transfer_via_mcp(directory):
    error = None

    if (directory != ''):
        # assemble transfer path
        transfer_path = os.path.join(
            get_server_config_value('watchDirectoryPath'),
            'activeTransfers/standardTransfer',
            directory,
        ) + '/'
        shared_directory_path = get_server_config_value('sharedDirectory')
        transfer_path = transfer_path.replace(shared_directory_path, '%sharedPath%', 1)

        # look up job UUID using transder path
        try:
            job = models.Job.objects.filter(directory=transfer_path, currentstep='Awaiting decision')[0]

            # approve transfer
            client = MCPClient()

            # 3rd arg should be uid?
            result = client.execute(job.pk, 'Approve', 3)

        except:
            error = 'Unabled to find unapproved transfer directory.'

    else:
        error = 'Please specify a transfer directory.'

    return error
