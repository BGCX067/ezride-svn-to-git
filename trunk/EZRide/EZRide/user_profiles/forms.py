#Developed by IntentoWeb
from django import forms
from django.forms import ModelForm
from registration.forms import RegistrationForm #@UnresolvedImport
from registration.models import RegistrationProfile #@UnresolvedImport
from models import UserProfile
from django.contrib.auth.models import User

attrs_dict = { 'class': 'required' }

class UserProfileRegistrationForm(RegistrationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))    
    
    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],                                                                   
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'])
        new_user.first_name=self.cleaned_data['first_name']
        new_user.last_name=self.cleaned_data['last_name']
        new_user.save()     
        new_user_profile = UserProfile(user=new_user)
        new_user_profile.save()   
        return new_user

class UserProfileEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        try:                                  
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email                        
        except User.DoesNotExist:
            pass
 
    first_name = forms.CharField(label="Nome",widget=forms.TextInput(attrs=attrs_dict))
    last_name = forms.CharField(label="Sobrenome",widget=forms.TextInput(attrs=attrs_dict))
    email = forms.EmailField(label="E-mail",help_text='')    
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 
                  'last_name',
                  'email']
        exclude = ('user')      
    
    def save(self, *args, **kwargs):
        user = self.instance.user       
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        profile = super(UserProfileEditForm, self).save(*args,**kwargs)
        return profile