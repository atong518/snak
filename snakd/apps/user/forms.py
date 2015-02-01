from django.utils.crypto import get_random_string
from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, Textarea, Select
from snakd.apps.user.models import GenericUser, CollegeUser, ProspieUser
from django.contrib.auth.forms import UserCreationForm
from django import forms

class GenericSignupForm(UserCreationForm):
    class Meta:
        model = GenericUser
        fields = ['email', 
                  'password1',
                  'password2',
                  'firstname', 
                  'lastname', 
                  'homecountry',
                  'homestate',
                 ]

    def save_user(self, data):
        user = GenericUser.objects.create_user(email=data['email'],
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               homestate=data['homestate'],
                                               password=data['password1'])
        return user

    def clean_password(self):
        cleaned_data = super(GenericSignupForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 == password2:
            print "pwd ok"
        else:
            raise forms.ValidationError("Your passwords do not appear to match :(")

        # always return the cleaned data
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(GenericSignupForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'true'})
        self.fields['lastname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'true'})
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'data-valid-error': "Yikes, that email address is invalid",
            'required': 'true'})
        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'true'})
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password again',
            'required': 'true',
            'data-match': '#id_password1',
            'data-error': 'Whoops, these passwords don\'t match'})

        self.fields.pop('username')


class CollegeSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = CollegeUser
        fields = GenericSignupForm.Meta.fields + ['bio']


    def clean_email(self):
        data = self.cleaned_data.get['email']
        if "@dartmouth.edu" not in data:
            msg = "ERROR"
            raise forms.ValidationError("ERROR")
        return super().clean()


    def save_user(self, data):
        user = CollegeUser.objects.create_user(email=data['email'],
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               homestate=data['homestate'],
                                               password=data['password1'],
                                               bio=data['bio'])
        user.save()
        return user
 
    def __init__(self, *args, **kwargs):
        super(CollegeSignupForm, self).__init__(*args, **kwargs)
        self.fields['homecountry'].widget = Select(attrs={
             'id': 'countrySelect1',
             'name': 'country',
             'onchange': "populateState(\'stateSelect1\', \'countrySelect1\')",
             'class': 'form-control',
             'required': 'true'})
        self.fields['homestate'].widget = Select(attrs={
             'id': 'stateSelect1',
             'name': 'state',
             'class': 'form-control'})
        self.fields['bio'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself!'})
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'pattern':'^[a-zA-Z0-9._\'-]+[0-9]@'+'dartmouth.edu'+'$',
            'data-error': "Please provide a full first.m.last.##@dartmouth.edu email address",
            'required': 'true'})



class ProspieSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = ProspieUser
        fields = GenericSignupForm.Meta.fields

    def save_user(self, data):
        user = ProspieUser.objects.create_user(email=data['email'],
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               homestate=data['homestate'],
                                               password=data['password1'])
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(ProspieSignupForm, self).__init__(*args, **kwargs)

        self.fields['homecountry'].widget = Select(attrs={
            'id': 'countrySelect2',
            'name': 'country',
            'onchange': "populateState(\'stateSelect2\', \'countrySelect2\')",
            'class': 'form-control',
            'required': 'true'})
        self.fields['homestate'].widget = Select(attrs={
            'id': 'stateSelect2',
            'name': 'state',
            'class': 'form-control'})
