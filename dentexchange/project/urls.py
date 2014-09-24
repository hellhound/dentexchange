# -*- coding:utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from ajax_upload import views as ajax_upload_views

from libs import admin
from libs.decorators import login_required_for, EMPLOYEE
from membership.decorators import enforce_membership

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login',
        name='logout_then_login'),
    url(r'^login', 'django.contrib.auth.views.login', name='login'),
    url(r'^auth/', include('authentication.urls', namespace='authentication')),
    url(r'^registration/',
        include('registration.urls', namespace='registration')),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^employer/',
        include('employer.urls', namespace='employer')),
    url(r'^employee/',
        include('employee.urls', namespace='employee')),
    url(r'^membership/',
        include('membership.urls',  namespace='membership')),
    url(r'^search/',
        include('search.urls', namespace='search')),
    url(r'matches/',
        include('matches.urls', namespace='matches')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'ajax_upload/',
        login_required_for(EMPLOYEE)(
        enforce_membership(ajax_upload_views.upload)),
        name='ajax-upload'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^robots\.txt', include('robots.urls')),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^privacy/$', 'flatpage', dict(url='/privacy/'), name='privacy'),
    url(r'^terms/$', 'flatpage', dict(url='/terms/'), name='terms'),
    url(r'^about/$', 'flatpage', dict(url='/about/'), name='about'),
)

if settings.DEBUG:
    # Media files 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += patterns('',
        url(r'^feedback/', include('feedback.urls')),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
