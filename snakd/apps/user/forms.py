from django.utils.crypto import get_random_string
from django.forms import ModelForm, EmailInput, TextInput, PasswordInput, Textarea, Select
from snakd.apps.user.models import GenericUser, CollegeUser, ProspieUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

UNLIMITED = 0
ONEDAY = 1
THREEDAYS = 3
ONEWEEK = 7
TWOWEEKS = 14

MAX_MATCH_FREQS = [
        (UNLIMITED, 'How often can we match you? - Unlimited'),
        (ONEDAY, '1 per day'),
        (THREEDAYS, '1 every 3 days'),
        (ONEWEEK, '1 per week'),
        (TWOWEEKS, '1 every 2 weeks'),
    ]

GENDER_CHOICES = [
    ("gender is a construct", "Gender - prefer not to disclose"),
    ("male", "Male"),
    ("female", "Female"),
]

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
                  'gender',
                 ]
            

    def save_user(self, data):
        user = GenericUser.objects.create_user(email=data['email'].lower(),
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               gender=data['gender'],
                                               homestate=data['homestate'],
                                               password=data['password1'])
        return user

    def checkstate(self):
        cleaned_data = super(GenericSignupForm, self).clean()
        if cleaned_data.get('homecountry') != "United States":
            del self.errors['homestate']

    def clean_password(self):
        cleaned_data = super(GenericSignupForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get('email').lower()
        if password1 and password2 and password1 == password2:
            print "pwd ok"
        else:
            raise forms.ValidationError("Your passwords do not appear to match :(")

        # always return the cleaned data
        return super().clean()

    def clean_state(self):
        console.log("TEST")
        cleaned_data = super(GenericSignupForm, self).clean()
        country = cleaned_data.get("homecountry")
        state = cleaned_data.get("homestate")
        if country == "United States" and not state:
            raise forms.ValidationError("State is a required field.")
        return cleaned_data

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

        self.fields.pop('username')


class CollegeSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = CollegeUser
        fields = GenericSignupForm.Meta.fields + ['bio'] + ['max_match_frequency']

    def save_user(self, data):
        user = CollegeUser.objects.create_user(email=data['email'].lower(),
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               homestate=data['homestate'],
                                               gender=data['gender'],
                                               password=data['password1'],
                                               bio=data['bio'],
                                               max_match_frequency=data['max_match_frequency'])
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
            'required': 'true'})#.lower()
        self.fields['max_match_frequency'].widget = Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'How often can we match you?'})
        self.fields['max_match_frequency'].widget.choices = MAX_MATCH_FREQS
        self.fields['gender'].widget = Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'Gender'})
        self.fields['gender'].widget.choices = GENDER_CHOICES
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


class ProspieSignupForm(GenericSignupForm):
    class Meta(GenericSignupForm.Meta):
        model = ProspieUser
        fields = GenericSignupForm.Meta.fields

    def save_user(self, data):
        user = ProspieUser.objects.create_user(email=data['email'].lower(),
                                               firstname=data['firstname'],
                                               lastname=data['lastname'],
                                               homecountry=data['homecountry'],
                                               homestate=data['homestate'],
                                               gender=data['gender'],
                                               password=data['password1'])
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(ProspieSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'pattern':'^((?!\@dartmouth\.edu).)*$',
            'data-error': "You're not a prospie! Try signing up as a College Student!",
            'required': 'true'})#.lower()   
        self.fields['gender'].widget = Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'Gender'})
        self.fields['gender'].widget.choices = GENDER_CHOICES
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
        self.fields['password1'].widget = PasswordInput(attrs={
            'id': 'prospie_password1',
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'true'})
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password again',
            'required': 'true',
            'data-match': '#prospie_password1',
            'data-error': 'Whoops, these passwords don\'t match'})

class GenericSettingsForm(UserChangeForm):
    class Meta():
        model = GenericUser
        fields = ['email', 
          'password',
          'firstname',
          'lastname',
          'id'
         ]

    def update_user(self):
        user = self.instance
        user.email = self.email
        return user


    def __init__(self, *args, **kwargs):
        super(GenericSettingsForm, self).__init__()
        self.instance = kwargs.get("instance", None)
        self.fields['email'].widget = EmailInput(attrs={
            'class': 'form-control',
            'initial': kwargs.get('email', "Email"),
            'data-valid-error': "Yikes, that email address is invalid",
            'required': 'true'})#.lower()
        self.fields['firstname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': 'true'})
        self.fields['lastname'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required': 'true'})
        self.fields['password'].widget = PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'true'})
        self.fields.pop('username')
        if self.instance:
            self.initial = self.instance.editableFields()

class CollegeSettingsForm(GenericSettingsForm):
    class Meta():
        model = CollegeUser
        fields = GenericSettingsForm.Meta.fields + [
          'bio',
          'max_match_frequency'
         ]

    def update_user(self, data):
        user = self.instance
        user.email = data['email'].lower()
        user.bio = data['bio']
        user.max_match_frequency = data['max_match_frequency']
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CollegeSettingsForm, self).__init__(*args, **kwargs)
        self.fields['max_match_frequency'].widget = Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'initial': MAX_MATCH_FREQS[0]})
        self.fields['max_match_frequency'].widget.choices = MAX_MATCH_FREQS
        self.fields['bio'].widget = Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about yourself!'})

class ProspieSettingsForm(GenericSettingsForm):
    class Meta():
        model = ProspieUser
        fields = GenericSettingsForm.Meta.fields + [
        ]


    def update_user(self, data):
        user = self.instance
        user.email = data['email'].lower()
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.firstname = data['firstname']
        user.lastname = data['lastname']
        user.save()
        return user


    def __init__(self, *args, **kwargs):
        super(ProspieSettingsForm, self).__init__(*args, **kwargs)

class ContactUsForm(ModelForm):
    class Meta():
        model = GenericUser
        fields = ['user_email','contact_comments']
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['user_email'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'true',
            'name': 'user_email'})
        self.fields['contact_comments'].widget = Textarea(attrs={
            'class': 'form-control',
            'style':'resize:none;',
            'placeholder': 'Let us know what is on your mind!',
            'required': 'true',
            'name': 'message'})
