from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, Textarea, Select
from django.contrib.auth.forms import UserCreationForm
from app.models import CollegeUser, ProspieUser

class CollegeSignupForm(UserCreationForm):
    class Meta:
        model = CollegeUser
        fields = ['email', 
                  'password1', 
                  'password2', 
                  'firstname', 
                  'lastname', 
                  'homecountry',
                  'homestate',
                  'bio']

    def __init__(self, *args, **kwargs):
        super(CollegeSignupForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'})
        self.fields['lastname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'})
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'})
        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password again'})
        self.fields['homecountry'].widget = Select(attrs={
             'id': 'countrySelect',
             'name': 'country',
             'onchange': 'populateState()',
             'class': 'form-control'})
        self.fields['homestate'].widget = Select(attrs={
             'id': 'stateSelect',
             'name': 'state',
             'class': 'form-control'})
        self.fields['bio'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself!'})
        self.fields.pop('username')

class ProspieSignupForm(UserCreationForm):
    class Meta:
        model = ProspieUser
        fields = ['email', 
                  'password1', 
                  'password2', 
                  'firstname', 
                  'lastname', 
                  'homecountry',
                  'homestate']

    def __init__(self, *args, **kwargs):
        super(ProspieSignupForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'})
        self.fields['lastname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'})
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'})
        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password again'})
        self.fields['homecountry'].widget = Select(attrs={
             'id': 'countrySelect',
             'name': 'country',
             'onchange': 'populateState()',
             'class': 'form-control'})
        self.fields['homestate'].widget = Select(attrs={
             'id': 'stateSelect',
             'name': 'state',
             'class': 'form-control'})
        self.fields.pop('username')
