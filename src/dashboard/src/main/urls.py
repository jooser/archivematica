from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template, redirect_to

UUID_REGEX = '[\w]{8}(-[\w]{4}){3}-[\w]{12}'

urlpatterns = patterns('main.views',

    # Index
    (r'^$', 'home'),

    # Forbidden
    (r'forbidden/$', 'forbidden'),

    # Jobs and tasks (is part of ingest)
    (r'jobs/(?P<uuid>' + UUID_REGEX + ')/explore/$', 'jobs_explore'),
    (r'jobs/(?P<uuid>' + UUID_REGEX + ')/list-objects/$', 'jobs_list_objects'),
    (r'tasks/(?P<uuid>' + UUID_REGEX + ')/$', 'tasks'),
    (r'task/(?P<uuid>' + UUID_REGEX + ')/$', 'task'),

    # Access
    (r'access/$', 'access_list'),
    (r'access/(?P<id>\d+)/delete/$', 'access_delete'),

    # Lookup
#    (r'lookup/rightsholder/(?P<id>\d+)/$', 'rights_holders_lookup'),

    # Autocomplete
#    (r'autocomplete/rightsholders$', 'rights_holders_autocomplete'),

    # Disabled until further development can be done
    #(r'administration/search/$', 'administration_search'),
    #(r'administration/search/flush/aips/$', 'administration_search_flush_aips'),

    # JSON feeds
    (r'status/$', 'status'),
    (r'formdata/(?P<type>\w+)/(?P<parent_id>\d+)/(?P<delete_id>\d+)/$', 'formdata_delete'),
    (r'formdata/(?P<type>\w+)/(?P<parent_id>\d+)/$', 'formdata'),
)

# Filesystem related JSON views
urlpatterns += patterns('main.filesystem',
    (r'filesystem/download/$', 'download'),
    (r'filesystem/contents/$', 'contents'),
    (r'filesystem/children/$', 'directory_children'),

    (r'filesystem/delete/$', 'delete'),
    (r'filesystem/copy_to_originals/$', 'copy_to_originals'),
    (r'filesystem/copy_to_arrange/$', 'copy_to_arrange'),
    (r'filesystem/copy_transfer_component/$', 'copy_transfer_component'),
    (r'filesystem/get_temp_directory/$', 'get_temp_directory'),
    (r'filesystem/ransfer/$', 'copy_to_start_transfer'),
    (r'filesystem/copy_from_arrange/$', 'copy_from_arrange_to_completed')
)