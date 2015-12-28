# Developed by Intento Web
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from registration.views import register #@UnresolvedImport
from profiles.views import edit_profile #@UnresolvedImport
from user_profiles.views import profile_index
from user_profiles.forms import UserProfileRegistrationForm, UserProfileEditForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'EZRide.views.home', name='home'),
    # url(r'^profiles/', include('user_profiles.urls')),    
    url(r'^accounts/register/$', register, {'form_class' : UserProfileRegistrationForm}, name='registration_register'),
    url(r'^accounts/', include('registration.urls')),   
    url(r'^profiles/edit/$', edit_profile, {'form_class': UserProfileEditForm,}, name='profiles_edit_profile'),
    url(r'^profiles/$', profile_index),
    url(r'^profiles/', include('profiles.urls')),   
    (r'^graphs/', include('graphs.urls')),              
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),      

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   # url(r'^admin/graphs/graph', include('graphs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
