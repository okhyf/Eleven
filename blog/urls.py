# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns(('blog.views'),
    url(r'^(?P<page>\d+)/$', 'article_list', name='articlelist'),
    url(r'^$', 'article_list', name='articlelist'),
    url(r'^article/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<id>\d+)/$', 'article_show', name='detailarticle'),
    url(r'^article/tag/(?P<id>\d+)/$', 'article_tag_filter', name='filtrarticletag'),
    url(r'^article/class/(?P<id>\d+)/$', 'article_class_filter', name='filtrarticleclass'),
    url(r'^article/archives/(?P<id>\d+)/$', 'article_archive_filter', name='filtrarticlearchive'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^article/add/$', 'article_add', name='addarticle'),
    url(r'^article/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<id>\w+)/update/$', 'article_update', name='updatearticle'),
    url(r'^article/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<id>\w+)/del/$', 'article_del', name='delarticle'),
    url(r'^article/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<id>\d+)/commentshow/$', 'article_show_comment', name='showcomment'),
)