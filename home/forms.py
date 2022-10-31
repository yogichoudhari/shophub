from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation
from .models import Address
class SignupForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100,widget=forms.TextInput(attrs={'class':'form-control signup-form-input mb-1','placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(label='Email',max_length=200,widget=forms.EmailInput(attrs={'class':'form-control signup-form-input mb-1','placeholder': 'Enter Your Email'}))
    phone = forms.CharField(label='Phone',max_length=10,widget=forms.TextInput(attrs={'class':'form-control signup-form-input mb-1','placeholder': 'Enter Your 10 digit Mobile Number'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control signup-form-input mb-1','placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control  mb-1 signup-form-input','placeholder': 'Re-enter Password'}),help_text='Password should be 6-20 charchters and alphanumeric')
    
    def clean_password(self):
        data = self.cleaned_data.get('confirm_password')
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)
        match = re.search(pattern, data)
        if not match:
            raise ValidationError('Password does not match requirements ')
        return data
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        try:
            data = int(data)
            if len(str(data))!=10:
                raise ValidationError('Please Enter A Valid Phone number')
        except ValueError as e:
            raise ValidationError('Phone Number Should be Numeric')
        return data
    
    def clean_email(self):
        data = self.cleaned_data.get('email')
        if '@gmail.com' not in data:
            raise ValidationError('Your email should be on gmail domain')
        return data

                
#    help_text=password_validation.password_validators_help_text_html()     
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",  widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control','placeholder':'Enter your old password'}))
    new_password1 = forms.CharField(label="New Password",  widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control','placeholder':'Enter new password'}))
    new_password2 = forms.CharField(label="Confirm New Password",  widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'Re-Enter your password'}))
    def clean_new_password1(self):
        data = self.cleaned_data['new_password1']
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)
        match = re.search(pattern, data)
        if not match:
            raise ValidationError('Password does not match requirements ')
        return data
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control','placeholder':'Enter Your Email'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control','placeholder':'Enter Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label="Confirm New Password",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control','placeholder':'Re-Enter Password'}))


#model form for address 

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {'name':forms.TextInput(attrs={'placeholder':'Enter Your Name','class':'form-control'}),
                   'house_no':forms.TextInput(attrs={'placeholder':'Enter Your House Number','class':'form-control'}),
                   'street':forms.TextInput(attrs={'placeholder':'Enter Street no. or Nearby place','class':'form-control'}),
                   'locality':forms.TextInput(attrs={'placeholder':'Enter locality or zone within your city','class':'form-control'}),
                   'city':forms.Select(attrs={'placeholder':'Select the City','class':'form-control'}),
                   'zip_code':forms.NumberInput(attrs={'placeholder':'Pin Code','class':'form-control'}),
                   'state':forms.TextInput(attrs={'class':'form-control','readonly': True})}

    