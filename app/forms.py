from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, Textarea, Select
from django.contrib.auth.forms import UserCreationForm
from app.models import GenericUser, CollegeUser, ProspieUser

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

    def clean(self):
        cleaned_data = super(ProspieSignupForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 == password2:
            print "pwd ok"
        else:
            raise forms.ValidationError("Your passwords do not appear to match :(")

        # always return the cleaned data
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(GenericSignupForm, self).__init__(*args, **kwargs)
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
        self.fields.pop('username')


class CollegeSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = CollegeUser
        fields = GenericSignupForm.Meta.fields + ['bio']

    def __init__(self, *args, **kwargs):
        super(CollegeSignupForm, self).__init__(*args, **kwargs)
        self.fields['homecountry'].widget = Select(attrs={
             'id': 'countrySelect1',
             'name': 'country',
             'onchange': "populateState(\'stateSelect1\', \'countrySelect1\')",
             'class': 'form-control'})
        self.fields['homestate'].widget = Select(attrs={
             'id': 'stateSelect1',
             'name': 'state',
             'class': 'form-control'})
        self.fields['bio'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself!'})

class ProspieSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = ProspieUser
        fields = GenericSignupForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super(ProspieSignupForm, self).__init__(*args, **kwargs)

        self.fields['homecountry'].widget = Select(attrs={
            'id': 'countrySelect2',
            'name': 'country',
            'onchange': "populateState(\'stateSelect2\', \'countrySelect2\')",
            'class': 'form-control'})
        self.fields['homestate'].widget = Select(attrs={
            'id': 'stateSelect2',
            'name': 'state',
            'class': 'form-control'})
