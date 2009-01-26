from django.conf.urls.defaults import *

urlpatterns = patterns('beardygeek.blog.views',
    url(r'^$', 'index', name='home'),
    url(r'^importer/$', 'importer', name='importer'),
)