# Developed by Intento Web
from django.conf.urls.defaults import patterns, include, url
from registration.views import register #@UnresolvedImport
from profiles.views import edit_profile #@UnresolvedImport
from forms import UserProfileRegistrationForm, UserProfileEditForm
from views import profile_index

urlpatterns = patterns('',                       
                       url(r'register/$', register, {'form_class' : UserProfileRegistrationForm}, name='registration_register'),
                       url(r'edit/$', edit_profile, {'form_class': UserProfileEditForm,}, name='profiles_edit_profile'),                           
                       url(r'^$', include('registration.urls', 'profiles.urls')),                       
)