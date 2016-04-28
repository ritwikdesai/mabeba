"""
Definition of urls for SemX.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from app import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'app.views.home', name='home'),
    #url(r'^admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login),
    url(r'^qr/$',views.qr),
    url(r'^secret/reset/$',views.request_secret_reset),
    url(r'^secret/reset/(?P<request_id>[-\w]+)(|/)$',views.secret_reset),
    url(r'^request/qr/$',views.request_qr),
    url(r'^request/qr/(?P<qr_id>[-\w]+)(|/)$',views.qr_request),
    url(r'^cookie/test/',views.cookie_test),
    url(r'^register/token/(?P<token_id>[-\w]+)(|/)$',views.register_token),
    url(r'^token/',views.token_request),
    url(r'^register/',views.register),
    url(r'^$',views.index,name='home'),
    url(r'^test/$',views.test),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
