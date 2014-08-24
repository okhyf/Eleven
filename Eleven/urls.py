from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Eleven.views.home', name='home'),
    url(r'^about$', 'Eleven.views.about', name='about'),
    url(r'^blog/', include('blog.urls')),
    url(r'^upload-pic$', 'Eleven.views.upload_pic', name='pictureupload'),
    url(r'^admin/', include(admin.site.urls)),
)
